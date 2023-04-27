import {
  VolStatus,
  type SingleVolunteer,
  type VolunteerInfoResponse,
  getVolStatusName,
} from "@/apis";

export function timeToHint(a: number) {
  const hr = Math.floor(a / 60);
  const mi = a % 60;
  if (hr != 0)
    if (mi != 0) return hr + " 小时 " + mi + " 分钟";
    else return hr + " 小时 ";
  else return mi + "分钟";
}

export function getStatusDisplayColor(status: VolStatus) {
  return {
    [VolStatus.Unaudited]: "black",
    [VolStatus.Audited]: "#007700",
    [VolStatus.Rejected]: "red",
    [VolStatus.Finished]: "#004400",
    [VolStatus.Deprecated]: "grey",
  }[status];
}

export function getVolStatusDisplayForUser(
  userId: number,
  volunteer: SingleVolunteer | VolunteerInfoResponse
) {
  if (volunteer.joiners.findIndex((v) => v.id === userId) !== -1) {
    if (volunteer.status === VolStatus.Audited) {
      return ["已报名", "brown"];
    }
    if (volunteer.status === VolStatus.Finished) {
      return ["已参与", "#33AA33"];
    }
  }
  return [
    getVolStatusName(volunteer.status),
    getStatusDisplayColor(volunteer.status),
  ];
}
