Bevy Version:0.12(current)


Param Sets
For safety reasons, a system cannot have multiple parameters
whose data access might have a chance of mutability conflicts over the
same data.
Some examples:

Multiple incompatible queries.
Using &World while also having other system parameters to access specific data.
…

Consider this example system:
fn reset_health(
    mut q_player: Query<&mut Health, With<Player>>,
    mut q_enemy: Query<&mut Health, With<Enemy>>,
) {
    // ...
}
The two queries are both trying to mutably access Health. They
have different filters, but what if there are entities that
have both Player and Enemy components? If we know that shouldn't happen, we
can add Without filters, but what if it is actually valid for our game?
Such code will compile (Rust cannot know about Bevy ECS semantics), but will
result in a runtime panic. When Bevy tries to run the system, it will panic with
a message about conflicting system parameters:
thread 'main' panicked at bevy_ecs/src/system/system_param.rs:225:5:
error[B0001]: Query<&mut game::Health, bevy_ecs::query::filter::With<game::Enemy>> in
system game::reset_health accesses component(s) game::Health in a way that conflicts
with a previous system parameter. Consider using `Without<T>` to create disjoint Queries
or merging conflicting Queries into a `ParamSet`.

Bevy provides a solution: wrap any incompatible parameters in a ParamSet:
fn reset_health(
    // access the health of enemies and the health of players
    // (note: some entities could be both!)
    mut set: ParamSet<(
        Query<&mut Health, With<Enemy>>,
        Query<&mut Health, With<Player>>,
        // also access the whole world ... why not
        &World,
    )>,
) {
    // set health of enemies (use the 1st param in the set)
    for mut health in set.p0().iter_mut() {
        health.hp = 50.0;
    }

    // set health of players (use the 2nd param in the set))
    for mut health in set.p1().iter_mut() {
        health.hp = 100.0;
    }

    // read some data from the world (use the 3rd param in the set)
    let my_resource = set.p2().resource::<MyResource>();
}
This ensures only one of the conflicting parameters can be used at the same time.
Bevy will now happily run our system.
The maximum number of parameters in a param set is 8.

### References
[[Systems  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] 