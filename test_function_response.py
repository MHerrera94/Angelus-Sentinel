import google.generativeai as genai
import asyncio

async def test():
    import os
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    
    def dummy_func(a: int) -> int:
        return a + 1
    
    model = genai.GenerativeModel('gemini-3.1-flash-lite', tools=[dummy_func])
    chat = model.start_chat()
    
    resp = await chat.send_message_async("Suma 2 a 3 usando dummy_func con a=2")
    print("AI dice:", resp.parts[0])
    
    if resp.parts[0].function_call:
        fc = resp.parts[0].function_call
        print("Llamó a función:", fc.name)
        
        # Opcion 1: dict directo
        try:
            resp2 = await chat.send_message_async(
                [{"function_response": {"name": fc.name, "response": {"result": 3}}}]
            )
            print("Dict funcionó:", resp2.text)
        except Exception as e:
            print("Dict falló:", e)
            try:
                import google.ai.generativelanguage as gl
                part = gl.Part(function_response=gl.FunctionResponse(name=fc.name, response={"result": 3}))
                resp2 = await chat.send_message_async(part)
                print("gl.Part funcionó:", resp2.text)
            except Exception as e2:
                print("gl.Part falló:", e2)
                
if __name__ == "__main__":
    asyncio.run(test())
