// All timestamps are stored in UTC on the backend; every display in the UI converts to IST here
// so there is a single place controlling the spec's "display in Asia/Kolkata" requirement.
export function formatIST(isoTimestamp: string): string {
  return new Date(isoTimestamp).toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }) + " IST";
}
