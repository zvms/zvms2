export function camal2Snake(str: string) {
    let result = str[0].toLowerCase();
    for (const c of str.slice(1)) {
        if (65 <= c.charCodeAt(0) && c.charCodeAt(0) <= 90) {
            result += "_";
        }
        result += c;
    }
    return result;
}

export function snake2Camal(str: string, largeCamal = false) {
    let result = "", upperCase = largeCamal;
    for (let c of str) {
        if (c === "_") upperCase = true;
        else {
            if (upperCase) {
                upperCase = false;
                c = c.toUpperCase();
            }
            result += c;
        }
    }
    return result;
}

export function alignRight(str: string, n: number, chr: string) {
    if (str.length > n)
        return str;
    return (chr.repeat(n) + str).slice(-1 * n);
}

export function number2ByteCode(num: number, n: number, suffix = "0b") {
    return suffix + alignRight(num.toString(2), n, "0");
}