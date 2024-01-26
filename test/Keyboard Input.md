Bevy Version:0.9(outdated!)


Keyboard Input
Relevant official examples:
keyboard_input,
keyboard_input_events.

This page shows how to handle keyboard keys being pressed and released.
If you are interested in text input, see the Character Input page instead.
Note: Command Key on Mac corresponds to the Super/Windows Key on PC.
Checking Key State
Most commonly, you might be interested in specific known keys and detecting when
they are pressed or released. You can check specific Key Codes or Scan
Codes using the
Input<KeyCode> / Input<ScanCode> resources.
fn keyboard_input(
    keys: Res<Input<KeyCode>>,
) {
    if keys.just_pressed(KeyCode::Space) {
        // Space was pressed
    }
    if keys.just_released(KeyCode::LControl) {
        // Left Ctrl was released
    }
    if keys.pressed(KeyCode::W) {
        // W is being held down
    }
    // we can check multiple at once with `.any_*`
    if keys.any_pressed([KeyCode::LShift, KeyCode::RShift]) {
        // Either the left or right shift are being held down
    }
    if keys.any_just_pressed([KeyCode::Delete, KeyCode::Back]) {
        // Either delete or backspace was just pressed
    }
}
Keyboard Events
To get all keyboard activity, you can use
KeyboardInput events:
fn keyboard_events(
    mut key_evr: EventReader<KeyboardInput>,
) {
    use bevy::input::ButtonState;

    for ev in key_evr.iter() {
        match ev.state {
            ButtonState::Pressed => {
                println!("Key press: {:?} ({})", ev.key_code, ev.scan_code);
            }
            ButtonState::Released => {
                println!("Key release: {:?} ({})", ev.key_code, ev.scan_code);
            }
        }
    }
}
These events give you both the Key Code and Scan Code.
Key Codes and Scan Codes
Keyboard keys can be identified by Key Code or Scan Code.
Key Codes represent the logical meaning of each key (usually the symbol/letter,
or function it performs). They are dependent on the keyboard layout currently
active in the user's OS. Bevy represents them with the KeyCode enum.
Scan Codes represent the physical key on the keyboard, regardless of the system
layout. Bevy represents them using ScanCode, which contains
an integer ID. The exact value of the integer is meaningless and OS-dependent,
but a given physical key on the keyboard will always produce the same value,
regardless of the user's language and keyboard layout settings.
Best Practices for Key Bindings
Here is some advice for how to implement user-friendly remappable key-bindings
for your game, that can work well for international users or those with
non-QWERTY keyboard layouts.
This section assumes that you have implemented some sort of system to allow the
user to reconfigure their keybindings. You want to prompt the user to press
their preferred key for a given in-game action, so you can store/remember it
and later use it for gameplay.
The problem is that, if you simply use Key Codes, then users might accidentally
switch their OS keyboard layout mid-game and suddenly have their keyboard not
work as expected.
You should detect and store the user's chosen keys using Scan Codes, and use
Scan Codes for detecting keyboard input during gameplay.
Key Codes can still be used for UI purposes, like to display the chosen key
to the user.

### References
[[Resources  Unofficial Bevy Cheat Book]] [[Text  Character  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] 