
export const NOT_EMPTY = () => (v: any) => !!v || "此处不能为空";
export const IS_NUMBER = () => (v: any) => !isNaN(parseFloat(v)) || "此处必须填数字";
export const IS_DECIMAL = () => (v: any) => !isNaN(parseInt(v)) || "此处必须填整数";
export const NOT_NEGATIVE = () => (v: any) => parseFloat(v) >= 0 || "此处不能为负";
export const IS_POSITIVE = () => (v: any) => parseFloat(v) > 0 || "此处必须为正数";
export const TIME = () => (v: any) => {
  try {
    if (!(typeof v === "string")) {
      throw new Error();
    }
    let x = v.split("-");
    if (x.length !== 5) throw new Error();
    let [ys, ms, ds, hs, mins] = x.map((v) => {
      let i = parseInt(v);
      if (!Number.isFinite(i)) {
        throw new Error();
      }
      return i;
    });
    if (!Number.isFinite(new Date(ys, ms, ds, hs, mins).getTime())) {
      throw new Error();
    }
  } catch (e: any) {
    return "时间格式错误或不完整";
  }
  return true;
};

//import { timeToHint } from "./calc";
export const IS_VAILD = () => (v: any) => {
  if (v == 114514 || v == 1919810) {
    return "请不要恶意填写时间！";
  //} else if (v > 360) {
  //  return `义工时间过长。有${timeToHint(v)}`;
  } else if (v <= 0) {
    return "义工时间小于等于0";
  } else if (v <= 5) {
    return "义工时间过短，此处的时间单位是分钟";
  }
  return true;
};