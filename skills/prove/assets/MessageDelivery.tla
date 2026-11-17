---------------------------- MODULE MessageDelivery ----------------------------
(* Example vflow level-A model: one outbound message whose status is updated by
   provider webhooks (which can arrive late or twice) and by a cleanup sweep that
   marks messages stuck in "sending" as failed.
   CONSTANT Fixed toggles the merge rule: FALSE = rank-based merge where "failed"
   outranks "delivered"/"read" (a late delivery report can never correct a sweep
   failure); TRUE = corrected merge.  Generic example, not tied to any codebase. *)
EXTENDS Naturals, TLC

CONSTANT Fixed

Statuses == {"queued", "sending", "delivered", "read", "failed"}
Reports  == {"delivered", "read", "failed"}
Rank == [queued |-> 0, sending |-> 1, delivered |-> 2, read |-> 3, failed |-> 4]

VARIABLES status,      \* what our system shows
          delivered,   \* ground truth: the provider delivered the message
          inflight     \* webhook reports sent by the provider, not yet applied

vars == <<status, delivered, inflight>>

Merge(s, r) ==
  IF Fixed
  THEN CASE s = "failed" /\ r \in {"delivered", "read"} -> r          \* late report corrects a sweep failure
         [] s \in {"delivered", "read"} /\ r = "failed"   -> s          \* a failure never undoes a delivery
         [] OTHER -> IF Rank[r] > Rank[s] THEN r ELSE s
  ELSE IF Rank[r] > Rank[s] THEN r ELSE s                              \* rank-only merge

Init == status = "queued" /\ delivered = FALSE /\ inflight = {}

WeSend          == status = "queued" /\ status' = "sending" /\ UNCHANGED <<delivered, inflight>>
ProviderDelivers == status # "queued" /\ ~delivered /\ "failed" \notin inflight
                    /\ delivered' = TRUE /\ inflight' = inflight \cup {"delivered"} /\ UNCHANGED status
ProviderReportsRead == delivered /\ inflight' = inflight \cup {"read"} /\ UNCHANGED <<status, delivered>>
ProviderFails   == status # "queued" /\ ~delivered /\ inflight' = inflight \cup {"failed"} /\ UNCHANGED <<status, delivered>>
SweepTimesOut   == status = "sending" /\ status' = "failed" /\ UNCHANGED <<delivered, inflight>>
WebhookArrives  == \E r \in inflight : status' = Merge(status, r) /\ inflight' = inflight \ {r} /\ UNCHANGED delivered
WebhookDuplicate == \E r \in inflight : status' = Merge(status, r) /\ UNCHANGED <<delivered, inflight>>
Done            == inflight = {} /\ status \in {"delivered", "read", "failed"} /\ UNCHANGED vars

Next == WeSend \/ ProviderDelivers \/ ProviderReportsRead \/ ProviderFails
        \/ SweepTimesOut \/ WebhookArrives \/ WebhookDuplicate \/ Done

Spec == Init /\ [][Next]_vars

TypeOK == status \in Statuses /\ delivered \in BOOLEAN /\ inflight \subseteq Reports

\* INV-4: once the provider's delivery report has been applied, we never show "failed".
DeliveryReportWins == (delivered /\ "delivered" \notin inflight) => status \in {"delivered", "read"}
=============================================================================
