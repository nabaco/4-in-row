﻿from .model_base import Model
import numpy as np
from random import choices


class KMeans(Model):
    """
    A model for K-Means clustering algorithm.
    Arguments:
        n_clusters (int): Num of clusters (K).
        n_features (int): Num of the features.
    """

    def __init__(self, n_clusters, n_features):
        self.n_clusters = n_clusters
        self.n_features = n_features
        self.cluster_centers = np.zeros((n_clusters, n_features))

    def random_init(self, X):
        """Random initialization of cluster centers"""
        return np.array(choices(X, k=self.n_clusters))

    def fit(self, X, n_iter, n_init):
        """
        Training the model by dataset X.
        Arguments:
            X (np.ndarray): Dataset.
            n_iter (int): Num of iteration.
            n_init (int): Num of algorithm iteration to avoid local minimum.
        """
        # Initialize loss value end final cluster_centers matrix
        loss = float("inf")
        cluster_centers = np.zeros((self.n_clusters, self.n_features))

        # Run k_means algorithm n_init times (to avoid local minimum) and save the best result
        for _ in range(n_init):
            self.k_means(X, n_iter)
            temp_cc = self.cluster_centers
            if self.loss(X, self.predict(X)) < loss:
                cluster_centers = temp_cc

        # Save the best result to the self.cluster_centers
        self.cluster_centers = cluster_centers

    def k_means(self, X, n_iter):
        """K-Means algorithm to minimize the loss function"""
        # Initialization of cluster centers
        self.cluster_centers = self.random_init(X)

        for _ in range(n_iter):
            # Associate each sample to cluster
            labels = self.predict(X)

            # Change cluster centers to the center of that samples
            samples_sum = np.zeros((self.n_clusters, self.n_features))
            count = np.zeros((self.n_clusters, 1))
            for sample, label in zip(X, labels):
                samples_sum[int(label)] += sample
                count[int(label)] += 1

            self.cluster_centers = samples_sum / count

    def predict(self, X):
        """Predict the labels of samples in the dataset X (np.ndarray)"""
        labels = []
        for sample in X:
            label = min(range(self.n_clusters), key=lambda k: np.linalg.norm(
                sample - self.cluster_centers[k])**2)
            labels.append(label)
        return np.array([labels]).T

    def loss(self, X, labels):
        """Compute the loss by labeles dataset X and the cluster_centers"""
        loss = 0
        for sample, label in zip(X, labels):
            loss += np.linalg.norm(sample -
                                   self.cluster_centers[int(label)])**2
        return loss
