Bevy Version:0.12(current)


Audio
Bevy offers a (somewhat barebones, but still useful) ECS-based Audio framework.
This chapter will teach you how to use it.
You can play sound effects and music from your game, with
volume control. There is a rudimentary "spatial audio"
implementation, which can pan sounds left/right in stereo, based on the
transforms of entities. You can also implement your
own custom sources of audio data, if you want to synthesize
sound from code, stream data from somewhere, or any other custom use case.
There are also 3rd-party alternatives to Bevy's audio support:

bevy_kira_audio: uses kira; provides a richer set of features and playback controls
bevy_oddio: uses oddio; seems to offer more advanced 3D spatial sound
bevy_fundsp: uses fundsp; for advanced sound synthesis and effects

(Bevy's official audio is based on the rodio library.)
As you can see, the Rust audio ecosystem is quite fragmented. There are
many backend libraries, all offering a different mix of features, none of
them particularly exhaustive. All of them are somewhat immature. You have
to pick your poison.
Audio is an area sorely in need of improvement. If you are an enthusiastic
audio developer, consider joining Discord and helping
with development!

### References
[[Transforms  Unofficial Bevy Cheat Book]] [[Spatial Audio  Unofficial Bevy Cheat Book]] [[Custom Audio Streams  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[Playing Sounds  Unofficial Bevy Cheat Book]] 