import pytest
import numpy as np
from models.k_means import KMeans
from sklearn.cluster import KMeans as SKKMeans


ACCEPTABLE_ERROR = 1e-20
N_ITER = 10
N_INIT = 1


@pytest.mark.parametrize(
    "n_clusters, n_features, n_samples",
    [
        (2, 2, 200),     # Two dimension 2-Means clustering
        (3, 3, 300),     # Three dimension 3-Means clustering

    ],
    ids=[
        '2dim/2means',
        '3dim/3means',
    ])
def test_k_means(n_clusters, n_samples, n_features):

    # Initialize the models
    cluster_centers = np.random.rand(n_clusters, n_features)

    model = KMeans(n_clusters, n_features)
    sk_model = SKKMeans(n_clusters, cluster_centers, N_INIT, N_ITER)

    # Random dataset
    X = np.random.rand(n_samples, n_features)
    if n_clusters == 2:
        X[n_samples//2:, :] += 0.5
    else:
        X[n_samples//3: 2*n_samples//3, :] += 0.5
        X[n_samples//3: 2*n_samples//3, :] -= 0.5

    # Fit the models
    model.fit(X, N_ITER, N_INIT, cluster_centers)
    sk_model.fit(X)

    # get cluster-centers and sort them
    centers = np.sort(model.cluster_centers, axis=0)
    sk_centers = np.sort(sk_model.cluster_centers_, axis=0)

    # Compare between the centers
    assert centers.shape == sk_centers.shape
    diff = 0
    for i in (centers - sk_centers):
        diff += np.linalg.norm(i)**2
    assert diff < ACCEPTABLE_ERROR
