Bevy Version:0.11(outdated!)


Text / Character Input
Relevant official examples:
char_input_events,
text_input.

Use this (not keyboard input) if you want to implement
text input in a Bevy app. This way, everything works as the user expects
from their operating system, including Unicode support.
Bevy will produce a ReceivedCharacter
event for every Unicode code point coming from the OS.
This example shows how to let the user input text into a string (here stored
as a local resource).
fn text_input(
    mut evr_char: EventReader<ReceivedCharacter>,
    kbd: Res<Input<KeyCode>>,
    mut string: Local<String>,
) {
    if kbd.just_pressed(KeyCode::Return) {
        println!("Text input: {}", &*string);
        string.clear();
    }
    if kbd.just_pressed(KeyCode::Back) {
        string.pop();
    }
    for ev in evr_char.iter() {
        // ignore control (special) characters
        if !ev.char.is_control() {
            string.push(ev.char);
        }
    }
}
Note: we are using Bevy's regular keyboard input to handle
the pressing of the enter and backspace keys. Character events are also sent
when these keys are pressed (they produce special control characters, like
ASCII newlines \n), so, if we don't want these to be saved to our string,
we need to ignore them.
In your own application, you might also want to handle things like arrow keys in
a way that is appropriate to your UI.
IME support
Bevy has support for IMEs (Input Method Editors), which is how people perform
text input in languages with more complex scripts, like East Asian languages. It
requires some special handling from you, however.
IMEs work by using a special "buffer", which shows the current in-progress text
suggestions and allows users to select the correct characters before confirming
them. The text suggestions / autocompletion is provided by the OS, but your app
needs to display them for the user.
If you'd like all international users to be able to input text in their
language, the way they usually do in other GUI apps on their OS, you should
support IMEs.
To do this, you need to enable "IME mode" on the window, whenever you are
expecting users to type text, and disable it afterwards. For example, if
you prompt users to enter their name, before playing the game, you enable
IME mode while the prompt is active.
While "IME mode" is enabled, if the user is using an IME, you will receive
Ime events, instead of ReceivedCharacter
and regular keyboard input. However, if the user is not using an IME, then
everything will behave as normal, even when "IME mode" is enabled.
While the user has in-progress text, you will get Ime::Preedit events, to tell
you the current contents of the "temporary buffer" and information about the
cursor/highlight you need to show, so that users can see what they are doing.
When the user confirms their input, you will get a Ime::Commit event, to tell
you the text that the user wishes to insert into the app.
// for this simple example, we will just enable/disable IME mode on mouse click
fn ime_toggle(
    mousebtn: Res<Input<MouseButton>>,
    mut q_window: Query<&mut Window, With<PrimaryWindow>>,
) {
    if mousebtn.just_pressed(MouseButton::Left) {
        let mut window = q_window.single_mut();

        // toggle "IME mode"
        window.ime_enabled = !window.ime_enabled;

        // We need to tell the OS the on-screen coordinates where the text will
        // be displayed; for this simple example, let's just use the mouse cursor.
        // In a real app, this might be the position of a UI text field, etc.
        window.ime_position = window.cursor_position().unwrap();
    }
}

fn ime_input(
    mut evr_ime: EventReader<Ime>,
) {
    for ev in evr_ime.iter() {
        match ev {
            Ime::Commit { value, .. } => {
                println!("IME confirmed text: {}", value);
            }
            Ime::Preedit { value, cursor, .. } => {
                println!("IME buffer: {:?}, cursor: {:?}", value, cursor);
            }
            Ime::Enabled { .. } => {
                println!("IME mode enabled!");
            }
            Ime::Disabled { .. } => {
                println!("IME mode disabled!");
            }
        }
    }
}
For the sake of brevity, this example just prints the events to the console.
In a real app, you will want to display the "pre-edit" text on-screen, and use
different formatting to show the cursor. On "commit", you can append the
provided text to the actual string where you normally accept text input.

### References
[[Keyboard  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Local Resources  Unofficial Bevy Cheat Book]] 