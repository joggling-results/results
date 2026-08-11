from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np
import polars as pl
import plotly.graph_objects as go

# =============================================================================
# Configuration
# =============================================================================

DATA_DIR = Path("data")
RESULTS_PATH = "data/results.csv"
IAAF_M_PATH = "data/IAAF_M_seconds.csv"
IAAF_F_PATH = "data/IAAF_F_seconds.csv"

RELAY_EVENTS = {
    "3b 4x100m",
    "3c 4x100m"
    "3b 4x200m",
    "3b 4x400m",
    "3c 4x400m"
}

EVENT_DICT = {
    "100m": ["3b 100m", "4b 100m", "5b 100m", "6b 100m", "7b 100m", "3c 100m"],
    "200m": ["3b 200m", "4b 200m", "5b 200m", "7b 200m"],
    "400m": ["3b 400m", "4b 400m", "5b 400m", "6b 400m", "7b 400m", "3c 400m"],
    "110mH": ["3b 110mH"],
    "400mH": ["3b 400mH"],
    "4x100m": ["3b 4x100m"],
    "4x200m": ["3b 4x200m"],
    "4x400m": ["3b 4x400m"],
    "600m": ["3b 600m", "4b 600m", "5b 600m"],
    "800m": ["3b 800m", "4b 800m", "5b 800m"],
    "1000m": ["3b 1000m"],
    "1500m": ["3b 1500m"],
    "Mile": ["3b Mile", "4b Mile", "5b Mile"],
    "3000m": ["3b 3km", "3c 3km"],
    "2 Miles": ["3b 2 Miles", "3c 2 Miles"],
    "5000m": ["3b 5km", "4b 5km", "5b 5km", "3c 5km"],
    "10 km": ["3b 10km", "4b 10km", "5b 10km", "3c 10km"],
    "15 km": ["3b 15km", "3c 15km"],
    "10 Miles": ["3b 10 Mile"],
    "HM": ["3b Half Marathon", "4b Half Marathon", "3c Half Marathon"],
    "Marathon": ["3b Marathon", "4b Marathon", "5b Marathon", "3c Marathon"],
}

RANKING_DISTANCES = [   
    "3b 100m", "3c 100m", "4b 100m", "5b 100m", "7b 100m",
    "3b 200m", "3c 200m", "4b 200m", "5b 200m",
    "3b 400m", "3c 400m", "4b 400m", "5b 400m",
    "3b 800m", "4b 800m", "5b 800m",
    "3b 1500m", "3b Mile", "3c Mile", "4b Mile", "5b Mile",
    "3b 4x100m", "3c 4x100m", "3b 4x400m",
    "3b 5km", "3c 5km", "4b 5km", "5b 5km",
    "3b 10km", "3c 10km", "4b 10km", "5b 10km",
    "3b Half Marathon", "3c Half Marathon", "4b Half Marathon",
    "3b Marathon", "3c Marathon", "5b Marathon",
]

# Use this for sorting the national records
DISTANCE_ORDER = pl.Enum(RANKING_DISTANCES)


# =============================================================================
# Loading / preparation
# =============================================================================

def load_results(path: Path = RESULTS_PATH) -> pl.DataFrame:
    """Load raw joggling results and add total_seconds."""

    print("Loading Raw Data")

    data = pl.read_csv(
        path,
        encoding="iso8859-1",
    )

    return data.with_columns(
        pl.col("Finish Time")
        .str.to_time()
        .cast(pl.Duration("ms"))
        .dt.total_seconds()
        .alias("total_seconds")
    )


def load_iaaf_tables() -> tuple[pl.DataFrame, pl.DataFrame]:
    """Load the male and female IAAF points tables."""

    print("Loading IAAF Points Data")

    iaaf_m = pl.read_csv(IAAF_M_PATH)
    iaaf_f = pl.read_csv(IAAF_F_PATH)

    return iaaf_m, iaaf_f


def remove_relays(data: pl.DataFrame) -> pl.DataFrame:
    """Remove relay events where nationality is not well defined."""

    return data.filter(
        ~pl.col("Distance").is_in(RELAY_EVENTS)
    )


# =============================================================================
# IAAF points
# =============================================================================

def find_iaaf_points(
    iaaf_perf_col: pl.Series,
    iaaf_points_col: pl.Series,
    joggler_time: float,
) -> int:
    """
    Assign IAAF points using the same bisect-style lookup as the
    original script.
    """

    # Preserve the original forward-fill behaviour.
    performance = iaaf_perf_col.fill_null(strategy="forward").to_list()
    points = iaaf_points_col.to_list()

    index = int(np.searchsorted(performance, joggler_time, side="left"))

    if index >= len(points):
        return 0

    value = points[index]

    if value is None or value > 1300:
        return 0

    return int(value)


def add_iaaf_points(
    data: pl.DataFrame,
    iaaf_m: pl.DataFrame,
    iaaf_f: pl.DataFrame,
) -> pl.DataFrame:
    """Add IAAF points to all recognised performances."""

    print("Adding IAAF Points Data")

    # Start with zero: unrecognised events remain zero.
    points = np.zeros(data.height, dtype=np.int64)

    distances = data.get_column("Distance").to_list()
    genders = data.get_column("Gender").to_list()
    times = data.get_column("total_seconds").to_list()

    male_tables = {
        event: (
            iaaf_m.get_column(event),
            iaaf_m.get_column("Points"),
        )
        for event in EVENT_DICT
    }
    female_tables = {
        event: (
            iaaf_f.get_column(event),
            iaaf_f.get_column("Points"),
        )
        for event in EVENT_DICT
    }

    for event, event_distances in EVENT_DICT.items():
        male_table = male_tables[event]
        female_table = female_tables[event]

        for i, (distance, gender, time) in enumerate(
            zip(distances, genders, times)
        ):
            if distance not in event_distances:
                continue

            if gender in {"M", "Mixed"}:
                points[i] = find_iaaf_points(
                    male_table[0],
                    male_table[1],
                    time,
                )
            elif gender == "F":
                points[i] = find_iaaf_points(
                    female_table[0],
                    female_table[1],
                    time,
                )

    return data.with_columns(
        pl.Series("IAAF Points", points)
    )


# =============================================================================
# IAAF rankings
# =============================================================================

def iaaf_best_performances(
    data: pl.DataFrame,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    """
    Create ranking tables for performances and best performance per joggler.
    """

    data = (
        remove_relays(data)
        .filter(pl.col("IAAF Points") > 0)
        .sort("IAAF Points", descending=True)
    )

    perf_rank = data.select([
        pl.col("IAAF Points"),
        pl.col("Distance"),
        pl.col("Finish Time"),
        pl.col("Joggler"),
        pl.col("Gender"),
        pl.col("Nationality"),
        pl.col("Date"),
        pl.col("Drops"),
        pl.col("Notes / Result Links"),
    ])

    # Pandas rank(method="average").astype(int) was effectively used here
    # after sorting. Dense row numbering is clearer for the sorted output.
    perf_rank = perf_rank.with_row_index("Rank", offset=1)

    # Best performance per joggler.
    joggler_rank = (
        perf_rank
        .unique(subset=["Joggler"], keep="first", maintain_order=True)
        .with_columns(
            pl.col("IAAF Points")
            .rank(method="ordinal", descending=True)
            .cast(pl.Int64)
            .alias("Rank")
        )
    )

    # Keep Rank first, matching the original output.
    perf_rank = perf_rank.select([
        "Rank",
        "IAAF Points",
        "Distance",
        "Finish Time",
        "Joggler",
        "Gender",
        "Nationality",
        "Date",
        "Drops",
        "Notes / Result Links",
    ])

    joggler_rank = joggler_rank.select([
        "Rank",
        "IAAF Points",
        "Distance",
        "Finish Time",
        "Joggler",
        "Gender",
        "Nationality",
        "Date",
        "Drops",
        "Notes / Result Links",
    ])

    return perf_rank, joggler_rank


# =============================================================================
# Joggler-level pivot
# =============================================================================

def make_joggler_pivot(data: pl.DataFrame) -> pl.DataFrame:
    """Create joggler-level statistics and personal bests."""

    data = remove_relays(data)

    joggler_df = (
        data
        .group_by(["Joggler", "Nationality", "Gender"])
        .agg([
            pl.col("Year").min().alias("First Active"),
            pl.col("Year").max().alias("Last Active"),
            pl.col("Event / Venue").count().alias("Entry Count"),
        ])
        .with_columns([
            pl.col("Nationality")
            .replace("0", "Unknown"),
            (
                pl.col("Last Active")
                - pl.col("First Active")
                + 1
            ).alias("Years Active"),
        ])
        .select([
            "Joggler",
            "Nationality",
            "Gender",
            "Years Active",
            "First Active",
            "Last Active",
            "Entry Count",
        ])
    )

    pivot_columns = [
        "3b 100m",
        "3c 100m",
        "3b 400m",
        "3b Mile",
        "3b 5km",
        "3b 10km",
        "3b Half Marathon",
        "3b Marathon",
        "5b 100m",
        "5b Mile",
        "5b 5km",
    ]

    pivot_df = (
        data
        .pivot(
            on="Distance",
            index="Joggler",
            values="Finish Time",
            aggregate_function="min",
        )
        .select(
            ["Joggler"]
            + [
                col for col in pivot_columns
                if col in data.get_column("Distance").unique().to_list()
            ]
        )
    )

    # Add missing expected columns so output shape remains stable.
    for col in pivot_columns:
        if col not in pivot_df.columns:
            pivot_df = pivot_df.with_columns(
                pl.lit("-").alias(col)
            )

    pivot_df = pivot_df.select(
        ["Joggler"] + pivot_columns
    ).with_columns(
        [
            pl.col(col).fill_null("-")
            for col in pivot_columns
        ]
    )

    return joggler_df.join(
        pivot_df,
        on="Joggler",
        how="left",
    )


# =============================================================================
# Country / year pivot
# =============================================================================

def make_country_year_pivot(data: pl.DataFrame) -> pl.DataFrame:
    """
    Create a pivot showing the number of active jogglers by country and year.
    """

    data = remove_relays(data)

    grouped_df = (
        data
        .select(["Joggler", "Nationality", "Year"])
        .group_by("Joggler")
        .agg([
            pl.col("Nationality").sort_by("Year").last().alias("Nationality"),
            pl.col("Year").max().alias("Year"),
        ])
        .with_columns(
            pl.col("Nationality").replace("0", "Unknown")
        )
    )

    return (
        grouped_df
        .group_by(["Year", "Nationality"])
        .len()
        .pivot(
            on="Nationality",
            index="Year",
            values="len",
            aggregate_function="sum",
        )
        .fill_null(0)
        .sort("Year")
    )


# =============================================================================
# All-time event rankings
# =============================================================================

def make_all_time_list(
    gender: str,
    distance: str,
    data: pl.DataFrame,
) -> pl.DataFrame:
    """
    Find each joggler's fastest performance for an event and rank it.
    """

    event_data = data.filter(
        (pl.col("Gender") == gender)
        & (pl.col("Distance") == distance)
    )

    if event_data.height == 0:
        # No results yet, so empty df.
        return pl.DataFrame({
            "Ranking": pl.Series([], dtype=pl.Int64),
            "Finish Time": pl.Series([], dtype=pl.String),
            "IAAF Points": pl.Series([], dtype=pl.Int64),
            "Joggler": pl.Series([], dtype=pl.String),
            "Gender": pl.Series([], dtype=pl.String),
            "Nationality": pl.Series([], dtype=pl.String),
            "Date": pl.Series([], dtype=pl.String),
            "Event / Venue": pl.Series([], dtype=pl.String),
            "Notes / Result Links": pl.Series([], dtype=pl.String),
        })

    fastest = (
        event_data
        # Sort by finish time (fastest to slowest) and keep only the fastest result per joggler
        .sort("Finish Time")
        .unique(subset=["Joggler"], keep="first", maintain_order=True)
        # Sort again (Unique may distort order)
        .sort("Finish Time")
        .with_row_index("Ranking", offset=1)
        .with_columns(
            pl.col("Nationality").replace("0", "Unknown")
        )
    )

    return fastest.select([
        "Ranking",
        "Finish Time",
        "IAAF Points",
        "Joggler",
        "Gender",
        "Nationality",
        "Date",
        "Event / Venue",
        "Notes / Result Links",
    ])


def create_all_time_lists(data: pl.DataFrame) -> None:
    """Create and save all-time rankings for each gender/event."""

    for gender in ["M", "F"]:
        for distance in RANKING_DISTANCES:
            file_string = (
                "ranking_"
                + gender
                + "_"
                + distance.replace(" ", "_")
            )

            fastest_times = make_all_time_list(
                gender,
                distance,
                data,
            )

            fastest_times.write_csv(
                DATA_DIR / f"{file_string}.csv"
            )
    
# =============================================================================
# National Records
# =============================================================================

def make_national_record_list(gender: str, nationality: str, data: pl.DataFrame,) -> pl.DataFrame:
    """
    Find each joggler's fastest performance for an event and rank it.
    """
    event_data = data.filter(
        (pl.col("Gender") == gender)
        & (pl.col("Nationality") == nationality)
        & (pl.col("Distance").is_in(RANKING_DISTANCES))
    )

    if event_data.height == 0:
        # No results yet, so empty df.
        return pl.DataFrame({
            "Ranking": pl.Series([], dtype=pl.Int64),
            "Finish Time": pl.Series([], dtype=pl.String),
            "IAAF Points": pl.Series([], dtype=pl.Int64),
            "Joggler": pl.Series([], dtype=pl.String),
            "Gender": pl.Series([], dtype=pl.String),
            "Nationality": pl.Series([], dtype=pl.String),
            "Date": pl.Series([], dtype=pl.String),
            "Event / Venue": pl.Series([], dtype=pl.String),
            "Notes / Result Links": pl.Series([], dtype=pl.String),
        })

    fastest = (
        event_data
        # Keep only the fastest result per event: these are national records
        .sort("Finish Time")
        .unique(subset=["Distance"], keep="first", maintain_order=True)
        .with_columns(pl.col("Distance").cast(DISTANCE_ORDER))
        .sort("Distance")
        .with_columns(pl.col("Distance").cast(pl.String))  # cast back so CSV output/downstream code sees plain strings
    )

    return fastest.select([
        "Distance",
        "Gender",
        "Finish Time",
        "IAAF Points",
        "Joggler",
        "Nationality",
        "Date",
        "Event / Venue",
        "Notes / Result Links",
    ])
    

def create_national_record_data(data:pl.DataFrame) -> None:
    """
    Saves a set of csvs for the Joggling national records, 1 file per gender, per country.
    """
    clean_national_data = data.filter(~pl.col('Nationality').is_in(['Mixed','0']))
    NATIONALITIES = clean_national_data['Nationality'].unique().to_list()
    print(NATIONALITIES)

    for gender in ["M", "F"]:
        for nationality in NATIONALITIES:
            file_string = (
                "records_"
                + gender
                + "_"
                + nationality.replace(" ", "_")
            )

            national_records = make_national_record_list(
                gender,
                nationality,
                clean_national_data,
            )

            national_records.write_csv(
                DATA_DIR / f"{file_string}.csv"
            )

    print("All National Record Lists Complete")


# =============================================================================
# Joggler network
# =============================================================================

def prepare_data(
    data: pl.DataFrame,
) -> tuple[list[str], pl.DataFrame]:
    """
    Prepare joggler and multi-joggler event data for the network graph.
    """

    data = remove_relays(data)

    jogglers = (
        data
        .get_column("Joggler")
        .unique()
        .to_list()
    )

    joggled_together = (
        data
        .filter(
            # Exclude events where not joggled together
            ~pl.col("Event / Venue").is_in(
                ["Time Trial", "IJA, Virtual"]
            )
        )
        .group_by(["Date", "Event / Venue"])
        .agg(
            pl.col("Joggler")
            .unique()
            .alias("Joggler")
        )
        .with_columns(
            pl.col("Joggler")
            .list.len()
            .alias("joggler_count")
        )
        .filter(pl.col("joggler_count") > 1)
    )

    return jogglers, joggled_together


def build_joggler_graph(
    jogglers: list[str],
    joggled_together: pl.DataFrame,
) -> nx.Graph:
    """
    Build a graph where nodes are jogglers and edge weights represent
    the number of events they have joggled together.
    """

    graph = nx.Graph()
    graph.add_nodes_from(jogglers)

    together_count: dict[tuple[str, str], int] = {}

    for event_jogglers in joggled_together.get_column("Joggler").to_list():
        for joggler_a, joggler_b in combinations(event_jogglers, 2):
            pair = tuple(sorted((joggler_a, joggler_b)))
            together_count[pair] = together_count.get(pair, 0) + 1

    for (joggler_a, joggler_b), count in together_count.items():
        graph.add_edge(
            joggler_a,
            joggler_b,
            weight=count,
        )

    return graph


def produce_plotly_figure(
    graph: nx.Graph,
    joggler_metadata: pl.DataFrame,
) -> go.Figure:
    """Create the interactive joggling community Plotly figure."""

    pos = nx.spring_layout(graph)

    nx.set_node_attributes(graph, pos, "pos")

    edge_x = []
    edge_y = []

    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]["pos"]
        x1, y1 = graph.nodes[edge[1]]["pos"]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []

    for node in graph.nodes():
        x, y = graph.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)

    node_adjacencies = []
    node_text = []

    metadata = {
        row["Joggler"]: (
            "?" if row["Nationality"] == "0" else row["Nationality"]
        )
        for row in joggler_metadata.select(
            ["Joggler", "Nationality"]
        ).to_dicts()
    }

    for node, adjacency in graph.adjacency():
        connections = len(adjacency)

        node_adjacencies.append(connections)

        nationality = metadata.get(node, "?")

        node_text.append(
            f"{node} ({nationality}): "
            f"# of connections: {connections}"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Greens",
            reversescale=False,
            color=node_adjacencies,
            size=10,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
            ),
            line_width=2,
        ),
        text=node_text,
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Interactive Joggling Community: "
                  "Who has joggled with who?",
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
        ),
    )

    fig.update_layout(
        autosize=False,
        width=800,
        height=500,
    )

    return fig


# =============================================================================
# Giduz number
# =============================================================================

def calculate_giduz_numbers(
    graph: nx.Graph,
    jogglers: list[str],
    data: pl.DataFrame,
) -> pl.DataFrame:
    """Calculate each joggler's Giduz number and shortest path."""

    source = "Bill Giduz"

    if source in graph:
        shortest_paths = nx.single_source_shortest_path(
            graph,
            source,
        )
    else:
        shortest_paths = {}

    rows = []

    metadata = (
        data
        .select(["Joggler", "Nationality", "Gender"])
        .unique(subset=["Joggler"])
        .to_dicts()
    )

    metadata_by_joggler = {
        row["Joggler"]: row
        for row in metadata
    }

    for joggler in jogglers:
        path = shortest_paths.get(joggler)

        if path is None:
            giduz_path = "No Connection to Bill Giduz"
            giduz_number = None
        else:
            giduz_path = " -> ".join(path)
            giduz_number = len(path) - 1

        row = metadata_by_joggler.get(
            joggler,
            {
                "Nationality": "Unknown",
                "Gender": None,
            },
        )

        rows.append({
            "Joggler": joggler,
            "Giduz_Path": giduz_path,
            "Giduz_Number": giduz_number,
            "Nationality": (
                "Unknown"
                if row["Nationality"] == "0"
                else row["Nationality"]
            ),
            "Gender": row["Gender"],
        })

    return (
        pl.DataFrame(rows)
        .sort("Giduz_Number")
    )


# =============================================================================
# Main pipeline
# =============================================================================

def main() -> None:
    """Run the complete joggling data-processing pipeline."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Load and prepare
    # -------------------------------------------------------------------------

    data = load_results()

    iaaf_m, iaaf_f = load_iaaf_tables()

    data = add_iaaf_points(
        data,
        iaaf_m,
        iaaf_f,
    )

    # Save enriched master data once.
    data.write_csv(RESULTS_PATH)

    # -------------------------------------------------------------------------
    # IAAF rankings
    # -------------------------------------------------------------------------

    perf_rank, joggler_rank = iaaf_best_performances(data)

    perf_rank.write_csv(
        DATA_DIR / "iaaf_perf_rank.csv"
    )

    joggler_rank.write_csv(
        DATA_DIR / "iaaf_joggler_rank.csv"
    )

    print("Joggling IAAF Best Performance Tables Complete")

    # -------------------------------------------------------------------------
    # Joggler pivot
    # -------------------------------------------------------------------------

    joggler_df = make_joggler_pivot(data)

    joggler_df.write_csv(
        DATA_DIR / "joggler_pivot.csv"
    )

    print("Joggler Pivot Complete")

    # -------------------------------------------------------------------------
    # Country / year pivot
    # -------------------------------------------------------------------------

    map_pivot_df = make_country_year_pivot(data)

    map_pivot_df.write_csv(
        DATA_DIR / "map_pivot.csv"
    )

    print("Joggler Map Data Complete")

    # -------------------------------------------------------------------------
    # All-time rankings
    # -------------------------------------------------------------------------

    create_all_time_lists(data)


    # -------------------------------------------------------------------------
    # National Records
    # -------------------------------------------------------------------------

    create_national_record_data(data)

    # -------------------------------------------------------------------------
    # Joggler network
    # -------------------------------------------------------------------------

    print("Producing Joggler Network Data...")

    jogglers, joggled_together = prepare_data(data)

    graph = build_joggler_graph(
        jogglers,
        joggled_together,
    )

    joggler_metadata = (
        data
        .select(["Joggler", "Nationality"])
        .unique(subset=["Joggler"])
    )

    fig = produce_plotly_figure(
        graph,
        joggler_metadata,
    )

    fig.write_html(
        DATA_DIR / "joggler_network.html"
    )

    print("Joggler Network Plot Complete")

    # -------------------------------------------------------------------------
    # Giduz numbers
    # -------------------------------------------------------------------------

    giduz_df = calculate_giduz_numbers(
        graph,
        jogglers,
        data,
    )

    giduz_df.write_csv(
        DATA_DIR / "giduz_df.csv"
    )

    # -------------------------------------------------------------------------

    print("ALL DATA PROCESSING COMPLETE!")


# Run Results Processing Pipeline
main()
