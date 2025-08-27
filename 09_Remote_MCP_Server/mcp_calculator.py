"""
Professional Calculator MCP Server Tool using FastMCP SDK
Provides basic arithmetic operations and advanced mathematical functions.
"""

from mcp.server.fastmcp import FastMCP
import math
import operator
from typing import Union, Dict, Any
import re

# Initialize FastMCP server
mcp = FastMCP("Calculator Server")

class CalculatorError(Exception):
    """Custom exception for calculator errors"""
    pass

class Calculator:
    """Professional calculator with support for basic and advanced operations"""
    
    # Safe operators mapping
    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '//': operator.floordiv,
        '%': operator.mod,
        '**': operator.pow,
        '^': operator.pow,  # Alternative power operator
    }
    
    # Safe math functions
    FUNCTIONS = {
        'abs': abs,
        'round': round,
        'floor': math.floor,
        'ceil': math.ceil,
        'sqrt': math.sqrt,
        'pow': pow,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'exp': math.exp,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'degrees': math.degrees,
        'radians': math.radians,
        'factorial': math.factorial,
        'gcd': math.gcd,
        'lcm': math.lcm if hasattr(math, 'lcm') else lambda a, b: abs(a * b) // math.gcd(a, b),
    }
    
    # Mathematical constants
    CONSTANTS = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau if hasattr(math, 'tau') else 2 * math.pi,
        'inf': math.inf,
        'nan': math.nan,
    }
    
    @staticmethod
    def evaluate_expression(expression: str) -> Union[float, int]:
        """
        Safely evaluate a mathematical expression
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            Union[float, int]: Result of the calculation
            
        Raises:
            CalculatorError: If expression is invalid or unsafe
        """
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        # Security: Check for dangerous patterns
        dangerous_patterns = [
            '__', 'import', 'exec', 'eval', 'open', 'file',
            'input', 'raw_input', 'compile', 'reload'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in expression.lower():
                raise CalculatorError(f"Unsafe expression: contains '{pattern}'")
        
        # Replace constants
        for const_name, const_value in Calculator.CONSTANTS.items():
            expression = expression.replace(const_name, str(const_value))
        
        # Replace ^ with ** for power operations
        expression = expression.replace('^', '**')
        
        try:
            # Use eval with restricted globals for safety
            allowed_names = {
                "__builtins__": {},
                **Calculator.FUNCTIONS,
                **Calculator.CONSTANTS
            }
            
            result = eval(expression, allowed_names)
            
            # Handle special cases
            if math.isnan(result):
                return "NaN"
            elif math.isinf(result):
                return "Infinity" if result > 0 else "-Infinity"
            
            # Return integer if result is a whole number
            if isinstance(result, float) and result.is_integer():
                return int(result)
            
            return result
            
        except ZeroDivisionError:
            raise CalculatorError("Division by zero")
        except ValueError as e:
            raise CalculatorError(f"Invalid mathematical operation: {str(e)}")
        except Exception as e:
            raise CalculatorError(f"Invalid expression: {str(e)}")

# MCP Tool: Basic Calculator
@mcp.tool()
def calculate(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression and return the result.
    
    Supports:
    - Basic arithmetic: +, -, *, /, //, %, ** (or ^)
    - Mathematical functions: sin, cos, tan, sqrt, log, exp, etc.
    - Constants: pi, e, tau
    - Parentheses for grouping
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4", "sin(pi/2)", "sqrt(16)")
    
    Returns:
        Dictionary containing the result and expression
    """
    try:
        result = Calculator.evaluate_expression(expression)
        return {
            "expression": expression,
            "result": result,
            "success": True
        }
    except CalculatorError as e:
        return {
            "expression": expression,
            "error": str(e),
            "success": False
        }

# MCP Tool: Advanced Calculator Operations
@mcp.tool()
def advanced_calculate(
    operation: str,
    operands: list,
    **kwargs
) -> Dict[str, Any]:
    """
    Perform advanced mathematical operations.
    
    Args:
        operation: Type of operation (sum, product, mean, median, mode, std_dev, variance)
        operands: List of numbers to operate on
        **kwargs: Additional parameters for specific operations
    
    Returns:
        Dictionary containing the operation result
    """
    try:
        if not operands:
            raise CalculatorError("No operands provided")
        
        # Convert to numbers
        nums = [float(x) for x in operands]
        
        if operation == "sum":
            result = sum(nums)
        elif operation == "product":
            result = 1
            for num in nums:
                result *= num
        elif operation == "mean" or operation == "average":
            result = sum(nums) / len(nums)
        elif operation == "median":
            sorted_nums = sorted(nums)
            n = len(sorted_nums)
            if n % 2 == 0:
                result = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
            else:
                result = sorted_nums[n//2]
        elif operation == "mode":
            from collections import Counter
            counts = Counter(nums)
            max_count = max(counts.values())
            modes = [k for k, v in counts.items() if v == max_count]
            result = modes[0] if len(modes) == 1 else modes
        elif operation == "std_dev" or operation == "standard_deviation":
            mean = sum(nums) / len(nums)
            variance = sum((x - mean) ** 2 for x in nums) / len(nums)
            result = math.sqrt(variance)
        elif operation == "variance":
            mean = sum(nums) / len(nums)
            result = sum((x - mean) ** 2 for x in nums) / len(nums)
        elif operation == "min":
            result = min(nums)
        elif operation == "max":
            result = max(nums)
        elif operation == "range":
            result = max(nums) - min(nums)
        else:
            raise CalculatorError(f"Unknown operation: {operation}")
        
        return {
            "operation": operation,
            "operands": operands,
            "result": result,
            "success": True
        }
        
    except Exception as e:
        return {
            "operation": operation,
            "operands": operands,
            "error": str(e),
            "success": False
        }

# MCP Tool: Number Base Conversion
@mcp.tool()
def convert_base(number: str, from_base: int, to_base: int) -> Dict[str, Any]:
    """
    Convert a number from one base to another.
    
    Args:
        number: Number as string in the source base
        from_base: Source base (2-36)
        to_base: Target base (2-36)
    
    Returns:
        Dictionary containing the conversion result
    """
    try:
        if from_base < 2 or from_base > 36 or to_base < 2 or to_base > 36:
            raise CalculatorError("Base must be between 2 and 36")
        
        # Convert to decimal first
        decimal_value = int(number, from_base)
        
        # Convert to target base
        if to_base == 10:
            result = str(decimal_value)
        else:
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if decimal_value == 0:
                result = "0"
            else:
                result = ""
                value = abs(decimal_value)
                while value > 0:
                    result = digits[value % to_base] + result
                    value //= to_base
                if decimal_value < 0:
                    result = "-" + result
        
        return {
            "original_number": number,
            "from_base": from_base,
            "to_base": to_base,
            "result": result,
            "decimal_value": decimal_value,
            "success": True
        }
        
    except Exception as e:
        return {
            "original_number": number,
            "from_base": from_base,
            "to_base": to_base,
            "error": str(e),
            "success": False
        }

