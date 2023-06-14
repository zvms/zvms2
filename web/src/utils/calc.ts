import {
  VolStatus,
  type SingleVolunteer,
  type VolunteerInfoResponse,
  getVolStatusName,
  ThoughtStatus,
} from "@/apis";

export function timeToHint(a: number) {
  const hr = Math.floor(a / 60);
  const mi = a % 60;
  if (hr !== 0)
    if (mi !== 0) return hr + " 小时 " + mi + " 分钟";
    else return hr + " 小时 ";
  else return mi + " 分钟";
}

export function getVolStatusDisplayColor(status: VolStatus) {
  return {
    [VolStatus.Unaudited]: "black",
    [VolStatus.Audited]: "#007700",
    [VolStatus.Rejected]: "red",
    [VolStatus.Finished]: "#004400",
    [VolStatus.Deprecated]: "grey",
  }[status] ?? "<NULL>";
}

export function getVolStatusDisplayText(
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
    getVolStatusDisplayColor(volunteer.status),
  ];
}

export function getThoughtStatusDisplayColor(status: ThoughtStatus) {
  return {
    [ThoughtStatus.Draft]: "#007700",
    [ThoughtStatus.Accepted]: "brown",
    [ThoughtStatus.WaitingForFinalAudit]: "#33AA33",
    [ThoughtStatus.WaitingForFirstAudit]: "null",
    [ThoughtStatus.WaitingForSignupAudit]: "null",
  }[status] ?? "<NULL>";
}

export const NoRetryTime = 5 * 60 * 1000;

export const MaxLoadingTime = 10 * 1000;
