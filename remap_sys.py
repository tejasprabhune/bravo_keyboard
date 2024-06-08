from dataclasses import dataclass
import random
import asyncio
import time
import keyboard

@dataclass
class KeySystem:
    """
    Passthrough system for BRAVO key press decoding
    in game systems. Mainly used for testing whether
    playing a game is feasible with certain limitations.

    decode_speed: float - Time it takes to decode a key press
    decode_acc: float - Accuracy of decoding
    mode_key: str - Key to toggle remap mode
    mode_remap: bool - Whether remap mode is on (for 8DOF vs 4DOF control)
    """
    decode_speed: float
    decode_acc: float
    mode_key: str
    mode_remap: bool

async def delay_time(delay):
    await asyncio.sleep(delay)

def delay_key(key, delay):
    async def handler():
        active_modifiers = sorted(
                modifier for modifier, 
                state in keyboard._listener.modifier_states.items() if state == 'allowed')

        for modifier in active_modifiers:
            keyboard.release(modifier)

        should_send = random.random() < key_system.decode_acc
        print("sending?", should_send)
        if should_send:
            await delay_time(delay)

            # If in remap mode, change WASD to arrow keys
            if key_system.mode_remap and key in wasd_remap:
                send_key = wasd_remap[key]
            else:
                send_key = key

            # Toggle remap mode
            if send_key == key_system.mode_key:
                key_system.mode_remap = not key_system.mode_remap
                print("changed mode to", key_system.mode_remap)
            else:
                keyboard.send(send_key)
                print("sent", send_key)

        for modifier in reversed(active_modifiers):
            keyboard.press(modifier)
        return False
    run_handler = lambda: asyncio.run(handler())
    keyboard.add_hotkey(key, run_handler, suppress=True, trigger_on_release=True)


if __name__ == "__main__":
    key_system = KeySystem(0.1, 0.9, "c", False)
    wasd_remap = {
        "w": "up",
        "a": "left",
        "s": "down",
        "d": "right"
    }
    keys = list("abcdefghijklmnopqrstuvwxyz")
    keys.extend(["left", "right", "up", "down"])
    for key in keys:
        delay_key(key, key_system.decode_speed)
    keyboard.wait('esc')
