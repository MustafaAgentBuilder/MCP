from mcp.server.fastmcp import FastMCP



mcp = FastMCP(name='Server_Prompts',stateless_http= True)




# Example 1: Simple prompt that only gets specific args
@mcp.prompt()
def write_story(character_name: str, setting: str, mood: str) -> str:
    """
    This prompt ONLY gets these 3 arguments - it cannot see anything else the user said!
    
    Args:
        character_name (str): Name of main character
        setting (str): Where story takes place  
        mood (str): What mood/tone for the story
    """
    # The prompt function creates its own instructions for the LLM
    # It doesn't know what the user originally asked for
    return f"""Write a creative short story with these specifications:

Main Character: {character_name}
Setting: {setting}
Mood/Tone: {mood}

Requirements:
- Make it exactly 300 words
- Include dialogue
- Have a clear beginning, middle, and end
- Make the character face a challenge
- End with a resolution

Write in third person narrative style."""

# Example 2: Complex prompt that transforms limited args into detailed instructions
@mcp.prompt()
def analyze_business_idea(idea: str, budget: str, timeline: str) -> str:
    """
    User only provides 3 simple inputs, but prompt creates comprehensive analysis request.
    
    Args:
        idea (str): Basic business idea description
        budget (str): Available budget
        timeline (str): When they want to launch
    """
    # The prompt adds its own expertise and structure
    return f"""Conduct a comprehensive business analysis for this venture:

BUSINESS CONCEPT: {idea}
AVAILABLE BUDGET: {budget}
TARGET TIMELINE: {timeline}

Please provide a detailed analysis covering:

1. MARKET ANALYSIS
   - Target audience identification
   - Market size and competition
   - Industry trends and opportunities

2. FINANCIAL PROJECTIONS
   - Startup costs breakdown
   - Revenue projections for first 3 years
   - Break-even analysis
   - Budget allocation recommendations

3. OPERATIONAL PLAN
   - Key milestones and timeline
   - Required resources and team
   - Critical success factors

4. RISK ASSESSMENT
   - Potential challenges and obstacles
   - Mitigation strategies
   - Alternative scenarios

5. RECOMMENDATIONS
   - Go/no-go decision framework
   - Next immediate steps
   - Success metrics to track

Format as a professional business report with clear sections and actionable insights."""

# Example 3: Educational prompt that adds pedagogy to simple topic request
@mcp.prompt()
def create_lesson_plan(subject: str, grade_level: str, duration: str) -> str:
    """
    Teacher just gives basic info, but prompt creates full pedagogical structure.
    
    Args:
        subject (str): What subject to teach
        grade_level (str): What grade/age group
        duration (str): How long the lesson should be
    """
    # Prompt adds educational expertise the user didn't specify
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

# Example 4: Technical prompt that adds engineering best practices
@mcp.prompt()
def code_review_request(code_type: str, language: str, complexity: str) -> str:
    """
    Developer gives minimal info, prompt creates comprehensive review criteria.
    
    Args:
        code_type (str): Type of code (web app, API, algorithm, etc.)
        language (str): Programming language used
        complexity (str): How complex the code is
    """
    # Prompt adds professional code review standards
    return f"""Perform a comprehensive code review for this {complexity} {code_type} written in {language}.

REVIEW CRITERIA:

1. CODE QUALITY
   - Readability and clarity
   - Naming conventions
   - Code organization and structure
   - Comments and documentation

2. FUNCTIONALITY
   - Logic correctness
   - Edge case handling
   - Error handling and validation
   - Performance considerations

3. BEST PRACTICES
   - Language-specific conventions
   - Design patterns usage
   - Security considerations
   - Maintainability factors

4. TESTING
   - Test coverage assessment
   - Missing test scenarios
   - Test quality and effectiveness

5. ARCHITECTURE
   - Code modularity
   - Separation of concerns
   - Scalability considerations
   - Integration patterns

REVIEW FORMAT:
- Overall assessment (1-10 score)
- Specific issues found (categorized by severity)
- Positive aspects to highlight
- Concrete improvement suggestions
"""




mcp_app = mcp.streamable_http_app()