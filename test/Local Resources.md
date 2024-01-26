Bevy Version:0.9(outdated!)


Local Resources
Relevant official examples:
ecs_guide.

Local resources allow you to have per-system data. This data
is not stored in the ECS World, but rather together with your system.
Local<T> is a system parameter similar to
ResMut<T>, which gives you full mutable access to an
instance of some data type, that is independent from entities and components.
Res<T>/ResMut<T> refer to a single global
instance of the type, shared between all systems. On the other hand, every
Local<T> parameter is a separate instance, exclusively for
that system.
#[derive(Default)]
struct MyState;

fn my_system1(mut local: Local<MyState>) {
    // you can do anything you want with the local here
}

fn my_system2(mut local: Local<MyState>) {
    // the local in this system is a different instance
}
The type must implement Default or
FromWorld. It is automatically initialized.
A system can have multiple Locals of the same type.
Specify an initial value
Local<T> is always automatically initialized using the
default value for the type.
If you need specific data, you can use a closure instead. Rust closures
that take system parameters are valid Bevy systems, just like standalone
functions. Using a closure allows you to "move data into the function".
This example shows how to initialize some data to configure a system,
without using Local<T>:
#[derive(Default)]
struct MyConfig {
    magic: usize,
}

fn my_system(
    mut cmd: Commands,
    my_res: Res<MyStuff>,
    // note this isn't a valid system parameter
    config: &MyConfig,
) {
    // TODO: do stuff
}

fn main() {
    let config = MyConfig {
        magic: 420,
    };

    App::new()
        .add_plugins(DefaultPlugins)
        // create a "move closure", so we can use the `config`
        // variable that we created above
        .add_system(move |cmd: Commands, res: Res<MyStuff>| {
            // call our function from inside the closure
            my_system(cmd, res, &config);
        })
        .run();
}
Another way to accomplish the same thing is to "return" the system
from "constructor" helper, that creates it:
#[derive(Default)]
struct MyConfig {
    magic: usize,
}

fn main() {
    // create a "constructor" closure, which can initialize
    // our data and move it into a closure that bevy can run as a system
    let constructor = || {
        // create the `MyConfig`
        let config = MyConfig {
            magic: 420,
        };

        // this is the actual system that bevy will run
        move |mut commands: Commands, res: Res<MyStuff>| {
            // we can use `config` here, the value from above will be "moved in"
            // we can also use our system params: `commands`, `res`
        }
    };

    App::new()
        .add_plugins(DefaultPlugins)
        // note the parentheses `()`
        // we are calling the "constructor" we made above,
        // which will return the actual system that gets added to bevy
        .add_system(constructor())
        .run();
}

### References
[[Systems  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 