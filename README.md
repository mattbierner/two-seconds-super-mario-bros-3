# Two Seconds of Super Mario Bros. 3

Scripts and data used for a [book containing every operation executed during two seconds of *Super Mario Bros. 3* for NES][project]

## Repo Contents

- `mario-book/`: Files for the [2 second Mario trace book][project].
- `mario-data/`: Raw screenshots and data for the Mario trace book.
- `lordtim,mitjitsu,tompa-supermariobros3.fm2`: Speed run gameplay movie used for the book.
- `fceux-screenshot-per-frame.lua`: FCEUX script that takes a screenshot per frame of gameplay.
- `*.py`: Python scripts used to generate the book.

## Capturing data from an NES game
This project uses the FCEUX emulator. To capture your own trace:

- Use the [FCEUX trace logger](http://www.fceux.com/web/help/TraceLogger.html) to capture the executed operations. Be sure to disable all logging fields except `Log frame count` and `To the left of dissasembly`.

- Use the `fceux-screenshot-per-frame.lua` Lua script to capture a screenshot of each frame of gameplay.

You should run the Lua script and the trace logger at the same time. Since the trace logger generates a lot of data and slows down the emulator quite a bit, you may need to use a pre-recorded gameplay movie instead of playing the game live.

## Converting captured data to a book
The `split_frame_data` python3 script splits a large trace file from the FCEUX trace logger into a one file per frame. To use it with the included example data:

```bash
$ unzip ./mario-data/speed/trace.log.zip -d ./mario-data/speed/

$ python split_frame_data.py \
    --trace-file=./mario-data/speed/trace.log \
    --out-dir=./scratch
```

The `frames_to_html` python3 script converts the frame data into an html page

```bash
$ python frames_to_html.py \
    --trace-files=./scratch/ \
    --out=./two-seconds-mario.html \
    --start=410 \
    --end=530 \
    --images-path=./mario-data/speed/
```

From here, you can open the html page or convert it to a PDF. Be aware the if you include a lot of frames, your browser may become unresponsive if you try viewing the generated html or try printing it. You can use headless chrome to convert the page to a pdf:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --no-margins --print-to-pdf=out.pdf ./out.html
```

## Example

- [pdf](https://github.com/mattbierner/two-seconds-super-mario-bros-3/blob/master/two-seconds-mario.pdf)
- [html](https://github.com/mattbierner/two-seconds-super-mario-bros-3/blob/master/two-seconds-mario.html)


[project]: https://blog.mattbierner.com/two-seconds-mario
