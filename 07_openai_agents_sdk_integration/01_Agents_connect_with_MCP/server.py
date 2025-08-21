from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    name = "Hello With OpenAi SDK",
    stateless_http = True
)



@mcp.tool(name="text_translator", description="Translate text between languages")
async def translate_text(text: str, target_language: str) -> str:
    # Integration with translation API
    return f"Translated '{text}' to {target_language}"




@mcp.tool(name="unit_converter", description="Convert between units")
async def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    # Example: temperature conversion
    conversions = {
        ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
    }
    
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result} {to_unit}"
    return "Conversion not supported"


@mcp.tool(name="calculator", description="Perform mathematical calculations")
async def calculate(expression: str) -> str:
    try:
        result = eval(expression)  # Be careful with eval in production
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"
    


app = mcp.streamable_http_app()