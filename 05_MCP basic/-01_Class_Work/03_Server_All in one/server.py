from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    name="All in one",
     stateless_http =True )


@mcp.prompt(name="lesson Plan")
def create_lesson_plan(subject: str, grade_level: str, duration: str) -> str:
    """
    Teacher just gives basic info, but prompt creates full pedagogical structure.
    
    Args:
        subject (str): What subject to teach
        grade_level (str): What grade/age group
        duration (str): How long the lesson should be
    """

    return f"""Design a comprehensive lesson plan with these parameters:

SUBJECT: {subject}
GRADE LEVEL: {grade_level}
LESSON DURATION: {duration}

Create a complete lesson plan following best educational practices:

LESSON STRUCTURE:
1. Opening Hook (5 minutes)
   - Attention-grabbing activity to engage students
   - Connection to prior knowledge

2. Learning Objectives
   - 3-4 specific, measurable objectives
   - Aligned with grade-level standards

3. Main Instruction ({duration} core time)
   - Step-by-step teaching sequence
   - Multiple learning modalities (visual, auditory, kinesthetic)
   - Interactive elements and student participation

4. Guided Practice
   - Scaffolded activities
   - Formative assessment opportunities

5. Independent Practice
   - Individual or small group work
   - Differentiation for various skill levels

6. Closure and Assessment
   - Summary of key concepts
   - Quick assessment method
   - Preview of next lesson

ADDITIONAL ELEMENTS:
- Required materials list
- Differentiation strategies for diverse learners
- Extension activities for advanced students
- Common misconceptions to address
- Homework or follow-up activities

Format as a ready-to-use lesson plan with clear timing and instructions."""



user_data = {
    "user_1": {"name": "Mustafa", "age": 18, "city": "Sialkot"},
    "user_2": {"name": "Ali", "age": 22, "city": "Karachi"},
    "user_3": {"name": "Ayesha", "age": 25, "city": "Islamabad"}
}

# Template resource that takes a user_id as input and fetches data
@mcp.resource(
    "user://get_user_info/{user_id}",
    mime_type="text/plain",
    name="get_user_info",
    description="Get user details like name, age, and city by user ID"
)
def get_user_info(user_id: str) -> str:
    # Try to get user data
    user = user_data.get(user_id)

    if user:
        return f"👤 Name: {user['name']}, Age: {user['age']}, City: {user['city']}"
    else:
        return "❌ User not found. Please check the ID."





@mcp.tool(name="calculator", description="Perform mathematical calculations")
async def calculate(expression: str) -> str:
    try:
        result = eval(expression)  # Be careful with eval in production
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


app = mcp.streamable_http_app()