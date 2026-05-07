from search import generate_candidate_routes
from ml import train_model, predict_delay, categorize_distance
from reasoning import evaluate_routes

# Change this to test different scenarios (morning, evening, etc.)
TIME_OF_DAY = "morning"


def main():
    # Warehouse grid with start (S), goal (G), walls (#), and open paths (.)
    warehouse_grid = [
        "####################",
        "#S.....#...........#",
        "#.###..#.#########.#",
        "#...#..#.....#.....#",
        "###.#..#####.#.#####",
        "#...#........#.....#",
        "#.##########.#####.#",
        "#..........#.......#",
        "#.######.#.#######.#",
        "#......#.#.....#...#",
        "######.#.#####.#.#.#",
        "#......#.....#...#.#",
        "#.##########.#.#.#.#",
        "#............#.#.#.#",
        "#................#G#",
        "####################",
    ]

    # Step 1: Generate candidate routes using BFS
    routes = generate_candidate_routes(warehouse_grid)

    # Step 2: Train ML model
    model, encoders, _ = train_model()

    # Step 3: Predict delay for each route
    for route in routes:
        distance_label = categorize_distance(route["distance"])
        route["distance_label"] = distance_label

        # Temporary assumptions for ML input (actual zone handled in reasoning)
        zone_type = "normal"
        congestion_level = "low" if distance_label == "short" else "medium"

        route["predicted_delay"] = predict_delay(
            model,
            encoders,
            time_of_day=TIME_OF_DAY,
            zone_type=zone_type,
            congestion_level=congestion_level,
            distance=distance_label,
        )

    # Step 4: Apply reasoning and print final output
    evaluate_routes(routes, TIME_OF_DAY)


if __name__ == "__main__":
    main()
