Bevy Version:0.9(outdated!)


Plugins
Relevant official examples:
plugin,
plugin_group.

As your project grows, it can be useful to make it more modular. You can
split it into "plugins".
Plugins are simply collections of things to be added to the App
Builder. Think of this as a way to add things to the app from
multiple places, like different Rust files/modules or crates.
struct MyPlugin;

impl Plugin for MyPlugin {
    fn build(&self, app: &mut App) {
        app
            .init_resource::<MyOtherResource>()
            .add_event::<MyEvent>()
            .add_startup_system(plugin_init)
            .add_system(my_system);
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugin(MyPlugin)
        .run();
}
Note how you get &mut access to the App, so you can
add whatever you want to it, just like you can do from your fn main.
For internal organization in your own project, the main value of plugins
comes from not having to declare all your Rust types and functions as
pub, just so they can be accessible from fn main to be added to the
app builder. Plugins let you add things to your app from multiple
different places, like separate Rust files / modules.
You can decide how plugins fit into the architecture of your game.
Some suggestions:

Create plugins for different states.
Create plugins for various sub-systems, like physics or input handling.

Plugin groups
Plugin groups register multiple plugins at once.
Bevy's DefaultPlugins and
MinimalPlugins are examples of this.
To create your own plugin group:
struct MyPluginGroup;

impl PluginGroup for MyPluginGroup {
    fn build(self) -> PluginGroupBuilder {
        PluginGroupBuilder::start::<Self>()
            .add(FooPlugin)
            .add(BarPlugin)
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(MyPluginGroup)
        .run();
}
When adding a plugin group to the app, you can disable some
plugins while keeping the rest.
For example, if you want to manually set up logging (with your own tracing
subscriber), you can disable Bevy's LogPlugin:
App::new()
    .add_plugins(
        DefaultPlugins.build()
            .disable::<LogPlugin>()
    )
    .run();
Note that this simply disables the functionality, but it cannot actually
remove the code to avoid binary bloat. The disabled plugins still have to
be compiled into your program.
If you want to slim down your build, you should look at disabling Bevy's
default cargo features, or depending on the various Bevy
sub-crates individually.
Plugin Configuration
Plugins are also a convenient place to store settings/configuration that are
used during initialization/startup. For settings that can be changed at runtime,
it is recommended that you put them in resources instead.

struct MyGameplayPlugin {
    /// Should we enable dev hacks?
    enable_dev_hacks: bool,
}

impl Plugin for MyGameplayPlugin {
    fn build(&self, app: &mut App) {
        // add our gameplay systems
        app.add_system(health_system);
        app.add_system(movement_system);
        // ...

        // if "dev mode" is enabled, add some hacks
        if self.enable_dev_hacks {
            app.add_system(player_invincibility);
            app.add_system(free_camera);
        }
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugin(MyGameplayPlugin {
            enable_dev_hacks: false, // change to true for dev testing builds
        })
        .run();
}
Plugins that are added using Plugin Groups can also be
configured. Many of Bevy's DefaultPlugins work
this way.
App::new()
    .add_plugins(DefaultPlugins.set(
        // here we configure the main window
        WindowPlugin {
            window: WindowDescriptor {
                width: 800.0,
                height: 600.0,
                // ...
                ..Default::default()
            },
            ..Default::default()
        }
    ))
    .run();
Publishing Crates
Plugins give you a nice way to publish Bevy-based libraries for other people
to easily include into their projects.
If you intend to publish plugins as crates for public use, you should read
the official guidelines for plugin authors.
Don't forget to submit an entry to Bevy Assets on the official
website, so that people can find your plugin more easily. You can do this
by making a PR in the Github repo.
If you are interested in supporting bleeding-edge Bevy (main), see here
for advice.

### References
[[Introduction  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Using bleedingedge Bevy main  Unofficial Bevy Cheat Book]] [[Plugins  Unofficial Bevy Cheat Book]] [[Customizing Bevy features modularity  Unofficial Bevy Cheat Book]] 