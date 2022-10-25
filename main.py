# coding: utf-8

from src.commands.command_list import OnCommandListener, LightCmd, SpecialCmd, CommandList, SPECIAL_CMD_TYPE_PAUSE
from src.commands.command_processor import CommandProcessor
from src.light.light_controller import LightController, MockLightController


class MyOnCommandListener(OnCommandListener):
    def __init__(self, light_controller: LightController):
        self.__light_controller = light_controller
        pass

    def on_light_command(self, light_cmd: LightCmd):
        print(light_cmd)
        self.__light_controller.show_effect(light_cmd.light)
    
    def on_pause_all(self):
        self.__light_controller.pause()

    def on_resume_all(self):
        self.__light_controller.resume()

if __name__ == '__main__':
    light_controller = MockLightController()
    light_controller.start()

    on_command_listener = MyOnCommandListener(light_controller)
    command_processor = CommandProcessor()

    command_processor.start()
    command_processor.add_on_command_list_listener(on_command_listener)

    # connection start

    # on receive msg
    command_processor.enqueue_command_list(CommandList(
        light_cmds=[
            LightCmd(
                delay=0,
                light="alert",
            ),
            LightCmd(
                delay=3000,
                light="turn_off",
            ),
        ],
        special_cmds=[
            SpecialCmd(
                type=SPECIAL_CMD_TYPE_PAUSE,
                all=True,
                delay=4000,
            ),
        ]
    ))

    command_processor.join()
    command_processor.remove_on_command_list_listener(on_command_listener)
