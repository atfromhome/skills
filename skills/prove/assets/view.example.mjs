// Example view module for the pstack `statechart` skill (used only when pstack is installed).
// Reader words, not variable or action names. See prove references/statechart.md.
export const title = "Message status";
export const state = (v) => ({ queued: "Queued", sending: "Sending", delivered: "Delivered", read: "Read", failed: "Failed" })[v.status];
export const step = (action, from, to) => ({
  WeSend: "we send",
  SweepTimesOut: "cleanup sweep times out",
  WebhookArrives: "a report arrives",
  WebhookDuplicate: "a report arrives again",
})[action] ?? null; // provider-side steps do not change what the reader sees
export const group = (v) => (["delivered", "read", "failed"].includes(v.status) ? "final" : "in flight");
export const colors = { final: "teal", "in flight": "blue" };
