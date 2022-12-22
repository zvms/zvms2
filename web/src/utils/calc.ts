
export function isTimeFinished(id: number, time: { inside: number, outside: number, large: number }) {
    // 义工时间上限；2021届以后有变动
    let vim = 24, vom = 20, vlm = 16;
    if (id > 20210000) { vim = 30; vom = 16; vlm = 18; }

    let inside = time.inside / 60.0;
    let outside = time.outside / 60.0;
    let large = time.large / 60.0;
    let result = true;
    if (outside < vom) { // 溢出判满机制：校内除二当校外
        inside = inside - (vom - outside) * 2;
        outside = vom;
    }
    if (large < vlm || inside < vim || outside < vom || inside + outside < vim + vom) {
        result = false;
    }
    return result;
}

export function timeToHint(a: number) {
    let hr = a / 60;
    let mi = a % 60;
    if (hr != 0)
        if (mi != 0)
            return hr + " 小时 " + mi + " 分钟";
        else
            return hr + " 小时 ";
    else
        return mi + "分钟";
}
