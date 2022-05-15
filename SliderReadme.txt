Each of the sliders that are used in Raw_Data_Entry_Sliders are customizable through a text file that is read line by line. Each slider is adjusted using the following line:

SliderName min max resolution

min - Value at the far left of the slider. Sliders start at this value

max - Value at the far right of the slider.

resolution - The minimum amount the slider can increment. Clicking the slider bar moves it by this amount.
    
min, max, and resolution can all be specified as doubles
    
Slider Names: CHIPAREA1, CHIPAREA2, DYNAMICPOWER1, DYNAMICPOWER2, STATICPOWER1, STATICPOWER2,       DYNAMICMEMORYPOWER1, DYNAMICMEMORYPOWER2, STATICMEMORYPOWER1, STATICMEMORYPOWER2, IPC1, IPC2

The names are NOT case sensitive

Each new slider requires a new line and a new command call

Any sliders not specified to the following default values:

CHIPAREA1, CHIPAREA2: min: 0, max: 5000, resolution: 0.01

DYNAMICPOWER1, DYNAMICPOWER2: min: 0, max: 200, resolution: 0.01

STATICPOWER1, STATICPOWER2: min: 0, max: 100, resolution: 0.01

DYNAMICMEMORYPOWER1, DYNAMICMEMORYPOWER2: min: 0, max: 30, resolution: 0.01

STATICMEMORYPOWER1, STATICMEMORYPOWER2: min: 0, max: 30, resolution: 0.01

IPC1, IPC2: min: 0, max: 1000, resolution: 1

Examples:

CHIPAREA1 5 1000 1

The slider ChipArea1 has a minimum value of 5, max of 1000, and the slider increments by 1

DYNAMICPOWER2 200 700 0.1

The slider DynamicPower2 has a minimum value of 200, max of 700, and the slider increments by 0.1
