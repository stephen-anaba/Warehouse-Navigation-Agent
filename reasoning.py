# This is the reasoning component of the project. 
# Its were logical rules (accept, reject & penalize) are applied
# It computes a weighted score for each route & selects best route.


# labels used to print routes as Route A, Route B, Route C
ROUTE_LABELS = ["A", "B", "C"]

# Postcondition: assigns a predefined zone type (normal, high_traffic, restricted)
# to a route based on its ID to simulate different scenarios.
def assign_zone_type(route_id):
    """
    Assign a zone type based on route ID.
    This is deterministic so that different routes consistently
    represent different scenarios (high traffic, normal, restricted).
    """
    mapping = {
        1: "high_traffic",  # route 1 simulates congestion
        2: "normal",        # route 2 is a safe/default path
        3: "restricted",    # route 3 simulates restricted access
    }

    # default to "normal" if route_id is not found
    return mapping.get(route_id, "normal")

# Postcondition: computes a weighted score (0–100) for a route based on distance, predicted delay, zone type, and time of day.
def compute_score(distance, delay, zone_type, time_of_day):
    """
    Compute a weighted score (0–100) for each route.
    Higher score = better route.

    Combines multiple factors:
    - Distance (shorter is better)
    - Delay prediction (lower is better)
    - Zone type (restricted is worst)
    - Time-of-day adjustments (scenario-based)
    """

    # start with a perfect score
    score = 100

    # distance penalty
    if distance == "long":
        score -= 25   # long routes are costly
    elif distance == "medium":
        score -= 10   # medium routes slightly penalized

    # delay penalty (from ML prediction)
    if delay == "high":
        score -= 40   # high delay is very bad
    elif delay == "medium":
        score -= 15

    # zone penalties
    if zone_type == "high_traffic":
        score -= 20   # congestion slows robot
    elif zone_type == "restricted":
        score -= 100  # effectively forces rejection

    # scenario-based adjustments
    # evening traffic is worse -> penalize high-traffic routes more
    if time_of_day == "evening" and zone_type == "high_traffic":
        score -= 20

    # morning routes with low delay get a small bonus
    if time_of_day == "morning" and delay == "low":
        score += 10

    # ensure score never goes below 0
    return max(score, 0)

# Postcondition: applies rule-based logic to decide whether a route is accepted or rejected, and provides a reason if rejected.
def make_decision(distance, delay, zone_type, score, time_of_day):
    """
    Apply rule-based reasoning to accept or reject a route.

    Returns:
    - decision: "accepted" or "rejected"
    - reason: explanation (only for rejected routes)
    """

    # scenario 3: hard constraint
    # any route through a restricted zone is immediately rejected
    if zone_type == "restricted":
        return "rejected", "passes restricted zone"

    # scenario 2: evening + high traffic + high delay
    if time_of_day == "evening" and zone_type == "high_traffic" and delay == "high":
        return "rejected", "high delay and high traffic zone"

    # general rule: avoid high delay
    if delay == "high":
        return "rejected", "high delay"

    # accept if score is strong enough
    if score >= 60:
        return "accepted", None

    # otherwise reject due to poor overall quality
    return "rejected", "low score"

# Postcondition: evaluates all candidate routes, prints their details,
# determines decisions, and selects the best route.
def evaluate_routes(routes, time_of_day):
    """
    Main reasoning pipeline:
    - Iterates through all candidate routes
    - Computes score + decision
    - Prints formatted output
    - Selects the best route
    """

    # print input condition (scenario)
    print(f"Input time_of_day: {time_of_day} \n")

    best_route = None
    best_score = -1  # track highest scoring accepted route

    # evaluate each route
    for i, route in enumerate(routes):
        label = ROUTE_LABELS[i]  # convert index -> A/B/C

        # extract route data
        path = route["path"]
        distance = route["distance_label"]
        delay = route["predicted_delay"]

        # assign zone type based on route ID
        zone_type = assign_zone_type(route["route_id"])

        # compute score using weighted system
        score = compute_score(distance, delay, zone_type, time_of_day)

        # apply logical rules to decide accept/reject
        decision, reason = make_decision(distance, delay, zone_type, score, time_of_day)

        # output format
        print(f"Route {label}: \nPath: {path}")
        print(f"Distance: {distance}")
        print(f"Zone type: {zone_type}")
        print(f"Predicted delay: {delay}")

        if decision == "rejected":
            # print rejection reason
            print("Decision: rejected")
            print(f"Reason: {reason}")
            print(f"Score: {score}")
        else:
            # print score only for accepted routes 
            print("Decision: accepted")
            print(f"Score: {score}")

            # track best route based on highest score
            if score > best_score:
                best_score = score
                best_route = label

        print()  # spacing between routes

    # final decision
    if best_route:
        print(f"Final Selected Route: Route {best_route}")
        print("Why: It avoids restricted zones and has a better final score than other available routes.")
    else:
        print("Final Selected Route: None")
        print("Why: All routes were rejected.")
