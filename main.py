from faster_whisper import WhisperModel
from zhconv import convert
from tencenttranslation import translation
"""
唉
"""
def seconds_to_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    timestamp = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return timestamp


head_str = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubStyle,Arial,20,&H0300FFFF,&H00FFFFFF,&H00000000,&H02000000,-1,0,0,0,100,100,0,0,3,2,0,2,10,10,10,1
Style: lulu,思源黑体 CN Heavy,40,&H00FFFFFF,&H000000FF,&H00F8A00E,&H00F81D11,0,0,0,0,100,100,0,0,1,5,2,2,10,10,40,1

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n'''

需要翻译 = True
model_size = "base"
input_file = "test.mp4"
model = WhisperModel(model_size, device="cuda", compute_type="float16")
segments, info = model.transcribe(input_file, beam_size=5)
print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
subline = ''

for segment in segments:
    print(f"{seconds_to_timestamp(segment.start)},{seconds_to_timestamp(segment.end)},{segment.text}\n")
    if 需要翻译:
        text = translation.translate([text])
    else:
        text = convert(segment.text, 'zh-cn')
    subline += f"Dialogue: 0,{seconds_to_timestamp(segment.start)},{seconds_to_timestamp(segment.end)},SubStyle,,0,0,0,,{text}\n"

ass = head_str + subline

output_file = input_file.split('.')[0] + ".ass"

with open(output_file, 'w', encoding='utf-8') as fw:
    fw.write(ass)
print(output_file)
print(".ass文件已创建并写入信息。")
