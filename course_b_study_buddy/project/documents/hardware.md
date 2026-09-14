# The Kestrel Project — Hardware

## The payload box

The standard Kestrel payload box is a cube of 20 cm expanded polystyrene, 30 mm thick,
weighing 340 g empty. It is wrapped in orange survival tape, both for visibility during
recovery and because orange showed up best against snow during the Flight 6 search.

The box holds four bays:

- **Bay A** — flight computer and batteries
- **Bay B** — primary camera, facing down through a cut-out
- **Bay C** — student experiment
- **Bay D** — trackers

## Flight computer

Kestrel uses a Raspberry Pi Pico running MicroPython. It logs temperature, pressure and
humidity once per second to an SD card. The team moved to the Pico from an Arduino Uno
after Flight 3, because the Uno's logging stopped whenever the internal temperature fell
below about -20 °C.

The flight computer does not control anything. It only records. This was a deliberate
decision after Flight 2, where a computer-controlled camera trigger failed and the flight
returned no photographs at all.

## Cameras

Two cameras fly on every flight:

- A **GoPro Hero 8** in Bay B, shooting 1080p video for the full flight
- A **Raspberry Pi Camera Module 3** taking one still photograph every 10 seconds

Both cameras are powered from their own batteries. Sharing a battery between cameras and
the flight computer was tried once, on Flight 5, and browned out the flight computer at
burst.

## Batteries

All Kestrel flights use lithium-based AA cells, never alkaline. Alkaline cells lose most of
their capacity below -30 °C, and the coldest temperature recorded on a Kestrel flight is
-58 °C, at 21,000 metres on Flight 7.

## Trackers

Two trackers fly on every flight, from different manufacturers:

- A **LoRa tracker** transmitting position every 30 seconds
- A **satellite tracker** transmitting every 5 minutes, as backup

The satellite tracker is slower and more expensive, but it works in valleys where the LoRa
signal does not reach. It is the only reason Flight 9 was recovered.
