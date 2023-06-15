from model.point import Point

from typing import List


def get_orientation(
    m_powers: List[List[float]],
    m_tag_vectors: List[List[Point]],
    m_normalized_distances: List[List[float]],
    m_intensities: List[List[float]],
):
    """
    Computes the orientation of the tag

    Each outer list represents data from multiple tag locations
    m_powers                  : each inner list contains powers of each light source
    m_tag_vectors             : each inner list contains vectors from tag to each light source
    m_normalized_distances    : each inner list contains normalized distances between tag and each light source
    m_intensities             : each inner list contains intensities recorded from each light source
    """

    num_positions = len(m_powers)

    if num_positions < 3:
        print("Error: Data from atleast 3 tag positions required.")
        return

    equations = []

    for i in range(num_positions):
        equations.append(
            process_position_data(
                m_powers[i],
                m_tag_vectors[i],
                m_normalized_distances[i],
                m_intensities[i],
            )
        )


def process_position_data(
    powers: List[float],
    tag_vectors: List[Point],
    normalized_distances: List[float],
    intensities: List[float],
):
    """
    Processes the data for one tag location

    powers                  : list of powers of each light source
    tag_vectors             : list of vectors from tag to each light source
    normalized_distances    : list of normalized distances between tag and each light source
    intensities             : list of intensities recorded from each light source
    """

    if len(powers) != len(tag_vectors) or len(tag_vectors) != len(normalized_distances):
        print("Error: Invalid data. All input lists must be of the same size.")
        return

    num_light_sources = len(powers)
    q_list: List[float] = []
    k = 1

    for i in range(num_light_sources):
        q_list.append((intensities[i] * normalized_distances[i] ** 2) / (k * powers[i]))

    # TODO: To be continued...
