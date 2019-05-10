# Algorithm Ideas
### Map numbers to scale degrees and modulations:
  - 0-6 : scale degrees
  - 7-9 : modulate to different scale (change active_scale)

### Chromatic intervals:
  - Start with note (or use first digit to compute)
  - Following digits are chromatic intervals up or down (mod 2 or random to choose up/down)

### Tuple Scale degree length:
  - Read in list of numbers in sets of 2
  - First number: scale degrees, (over 7 -> modulates active_scale)
  - Second number: modulates active_length, active_length_mod?
    - 0-5: 1, 1/2, 1/4, 1/8, 1/16, 1/32
    - 6,7,8,9: none, none, triplet, dotted
