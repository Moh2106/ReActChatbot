from typing import List, Any, Dict, Tuple

from llama_index.core.llama_pack import BaseLlamaPack
from tools import Setings
from . import Agent

import sys
import io


class GradioReActAgentPack(BaseLlamaPack):
    """Gradio chatbot to chat with a ReActAgent pack."""

    def __init__(
        self,
        #tools_list: Optional[List[str]] = list(SUPPORTED_TOOLS.keys()),
        **kwargs: Any,
    ) -> None:
        """Init params."""
        try:
            from ansi2html import Ansi2HTMLConverter
        except ImportError:
            raise ImportError("Please install ansi2html via `pip install ansi2html`")

        """tools = []
        for t in tools_list:
            try:
                tools.append(SUPPORTED_TOOLS[t]())
            except KeyError:
                raise KeyError(f"Tool {t} is not supported.")
        self.tools = tools"""

        self.llm = Setings.get_llm()
        self.agent = Agent.Agent().initialize_agents()

        self.thoughts = ""
        self.conv = Ansi2HTMLConverter()

    def get_modules(self) -> Dict[str, Any]:
        """Get modules. , "tools": self.tools"""
        return {"agent": self.agent, "llm": self.llm}

    def _handle_user_message(self, user_message, history):
        """Handle the user submitted message. Clear message box, and append
        to the history.
        """
        return "", [*history, (user_message, "")]

    def _generate_response(
        self, chat_history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """Generate the response from agent, and capture the stdout of the
        ReActAgent's thoughts.
        """
        """Generate the response from agent, and capture the stdout of the ReActAgent's thoughts."""

        class Capturing(list):
            def __enter__(self):
                self._stdout = sys.stdout
                sys.stdout = self._stringio = io.StringIO()
                return self

            def __exit__(self, *args):
                self.extend(self._stringio.getvalue().splitlines())
                sys.stdout = self._stdout


        with Capturing() as output:
            response = self.agent.stream_chat(chat_history[-1][0])
        ansi = "\n========\n".join(output)
        html_output = self.conv.convert(ansi)
        for token in response.response_gen:
            chat_history[-1][1] += token
            yield chat_history, str(html_output)

    def _reset_chat(self) -> tuple[str, str, str]:
        """Reset the agent's chat history. And clear all dialogue boxes."""
        # clear agent history
        self.agent.reset()
        return "", "", ""  # clear textboxes

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        import gradio as gr
        #gstaff/xkcd

        demo = gr.Blocks(
            theme="gr.themes.Soft()",
            css="#box { height: 500px; overflow-y: scroll !important}",
        )

        with demo:

            gr.Markdown(
                "# Welcome in our online shop "
            )
            with gr.Row():
                chat_window = gr.Chatbot(
                    label="Message History",
                    scale=6,
                )
                console = gr.HTML(elem_id="box")
            with gr.Row():
                message = gr.Textbox(label="Write A Message", scale=4)
                clear = gr.ClearButton()

            message.submit(
                self._handle_user_message,
                [message, chat_window],
                [message, chat_window],
                queue=False,
            ).then(
                self._generate_response,
                chat_window,
                [chat_window, console],
            )
            clear.click(self._reset_chat, None, [message, chat_window, console])

        demo.launch(server_name="0.0.0.0", server_port=8080, share=True)