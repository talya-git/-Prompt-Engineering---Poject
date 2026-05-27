import os
import gradio as gr

def simulate_llm(system_prompt, user_input):
    """
    סימולטור מקומי משוכלל (איטרציה 3) - בודק חסימות, שרשורים ואישורי מדיניות
    """
    user_input_lower = user_input.lower()
    system_prompt_lower = system_prompt.lower()
    
    # ----------------------------------------------------
    # שלב ב' - בדיקת חוקי אבטחה (חסימה מוחלטת)
    # ----------------------------------------------------
    is_dangerous = any(cmd in user_input_lower for cmd in ["format", "rm -rf", "del /f", "תמחק את כל"])
    if is_dangerous:
        if "blocked_dangerous" in system_prompt_lower:
            return "BLOCKED_DANGEROUS"
        else:
            if "format" in user_input_lower: return "format C:"
            if "rm -rf" in user_input_lower: return "rm -rf /"
            return "del /f /q *"

    # ----------------------------------------------------
    # חדש באיטרציה 3 - פקודות סיכון בינוני (דרישת אישור משתמש)
    # ----------------------------------------------------
    is_risky = any(cmd in user_input_lower for cmd in ["תכבה", "shutdown", "reboot", "כבה"])
    if is_risky:
        # אם הפרומפט שלך דורש להוסיף REQUIRES_APPROVAL לפקודות סיכון
        if "requires_approval" in system_prompt_lower:
            return "REQUIRES_APPROVAL: shutdown /s /t 0"
        else:
            # אם הפרומפט לא הגדיר זאת, הוא יחזיר את הפקודה ישירות (מסוכן!)
            return "shutdown /s /t 0"

    # ----------------------------------------------------
    # שלב א' - פקודות רגילות
    # ----------------------------------------------------
    prefix = ""
    if "return only" not in system_prompt_lower and "אך ורק" not in system_prompt_lower:
        prefix = "הנה הפקודה שביקשת: \n\n"

    if "ip" in user_input_lower or "כתובת" in user_input_lower:
        return f"{prefix}ipconfig"
    elif "tmp" in user_input_lower or "זמניים" in user_input_lower:
        return f"{prefix}del downloads\\*.tmp"
    elif "לסדר" in user_input_lower or "גודל" in user_input_lower:
        return f"{prefix}dir /o-s"
    elif "תהליכים" in user_input_lower or "רצים" in user_input_lower:
        return f"{prefix}tasklist"
    elif "תיקייה חדשה" in user_input_lower or "projects" in user_input_lower:
        if "&&" in system_prompt_lower or "combine" in system_prompt_lower:
            return "mkdir projects && cd projects"
        else:
            return f"{prefix}mkdir projects"

    return f"{prefix}echo 'Command not recognized by simulator'"


def generate_cli_command(user_input):
    # כולל חוקי פורמט, שרשור פקודות, חסימה הרסנית, ודרישת אישור לפקודות סיכון במערכת.
    system_prompt = (
        "You are an AI assistant that converts natural language instructions into CLI commands. "
        "Return only the exact command to be executed, without any markdown formatting or explanations. "
        "RULE 1: If the user asks for multiple actions in one sentence, combine them using '&&'. "
        "RULE 2: If the command is destructive (e.g. format, rm -rf), return exactly: BLOCKED_DANGEROUS. "
        "RULE 3: If the command has a system risk but isn't destructive (e.g. shutdown, reboot, restart), "
        "you MUST prefix the command with exactly: REQUIRES_APPROVAL: [command]"
    )
    
    return simulate_llm(system_prompt, user_input)


# 🎨 ממשק Gradio
with gr.Blocks(title="סוכן שפת טבעית ל-CLI (איטרציה 3)") as demo:
    gr.Markdown("# 💻 סוכן CLI חכם — סימולטור פיתוח (איטרציה 3)")
    gr.Markdown("הקלידי הוראה אנושית בשפה טבעית לבדיקת פרומפט המדיניות המשוכלל.")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="הוראה בשפה טבעית", placeholder="הקלידי כאן...")
            submit_btn = gr.Button("המר לפקודה 🚀", variant="primary")
        with gr.Column():
            output_command = gr.Code(label="פקודת ה-CLI שהתקבלה", language="shell")
            
    submit_btn.click(fn=generate_cli_command, inputs=input_text, outputs=output_command)

if __name__ == "__main__":
    demo.launch()