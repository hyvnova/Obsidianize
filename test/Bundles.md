Bevy Version:0.12(current)


Relevant official examples:
ecs_guide.

Bundles
You can think of Bundles like "templates" or "blueprints" for creating entities.
They make it easy to create entities with a common set of
components.
By creating a bundle type, instead of adding your components one by one, you
can make sure that you will never accidentally forget some important component
on your entities. The Rust compiler will give an error if you do not set all
the fields of a struct, thus helping you make sure your code is correct.
Bevy provides many built-in bundle types that you can use
to spawn common kinds of entities.
Here is how to create your own bundle:
#[derive(Bundle)]
struct PlayerBundle {
    xp: PlayerXp,
    name: PlayerName,
    health: Health,
    marker: Player,

    // We can nest/include another bundle.
    // Add the components for a standard Bevy Sprite:
    sprite: SpriteSheetBundle,
}
You can then use your bundle when you spawn your entities:
commands.spawn(PlayerBundle {
    xp: PlayerXp(0),
    name: PlayerName("Player 1".into()),
    health: Health {
        hp: 100.0,
        extra: 0.0,
    },
    marker: Player,
    sprite: SpriteSheetBundle {
        // TODO
        ..Default::default()
    },
});
If you want to have default values (similar to Bevy's bundles):
impl Default for PlayerBundle {
    fn default() -> Self {
        Self {
            xp: PlayerXp(0),
            name: PlayerName("Player".into()),
            health: Health {
                hp: 100.0,
                extra: 0.0,
            },
            marker: Player,
            sprite: Default::default(),
        }
    }
}
Now you can do this:
commands.spawn(PlayerBundle {
    name: PlayerName("Player 1".into()),
    ..Default::default()
});
Loose components as bundles
Technically, Bevy also considers arbitrary tuples of components as bundles:
(ComponentA, ComponentB, ComponentC)

This allows you to easily spawn an entity using a loose bunch of components (or
bundles), or add more arbitrary components when you spawn entities. However,
this way you don't have the compile-time correctness advantages that a
well-defined struct gives you.
commands.spawn((
    SpriteBundle {
        // ...
        ..default()
    },
    Health {
        hp: 50.0,
        extra: 0.0,
    },
    Enemy,
    // ...
));
You should strongly consider creating proper structs, especially if you are
likely to spawn many similar entities. It will make your code easier to maintain.
Querying
Note that you cannot query for a whole bundle. Bundles are just a
convenience when creating the entities. Query for the individual component types
that your system needs to access.
This is wrong:
fn my_system(query: Query<&SpriteBundle>) {
  // ...
}
Instead, do this:
fn my_system(query: Query<(&Transform, &Handle<Image>)>) {
  // ...
}
(or whatever specific components you need in that system)

### References
[[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 