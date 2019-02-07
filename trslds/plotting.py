import numpy as np
import numpy.random as npr
import utils
from numpy import newaxis as na

def contour_plt(R, xmin, xmax, ymin, ymax, delta, depth, leaf_path, K):
    x, y = np.arange(xmin,xmax, delta), np.arange(ymin,ymax, delta)
    X,Y = np.meshgrid(x,y)
    points = np.zeros( (X[:,0].size, X[0,:].size, 2) )
    points[:,:,0] = X
    points[:,:, 1] = Y
    colors = np.zeros( ( X[:,0].size, X[0,:].size, K   ) )
    
    for rows in range( X[:,0].size):
        for cols in range( X[0,:].size):
            pts = points[rows,cols,:] 
            #Compute log of probabilities
            log_prior_prob = utils.compute_leaf_log_prob(R, pts, K, depth, leaf_path)
            p_unnorm = np.exp( log_prior_prob - np.max(log_prior_prob) )
            p_norm = p_unnorm / np.sum(p_unnorm)
            colors[rows,cols,:] = np.array(p_norm).flatten()
    return x, y, colors

def rot_contour_plt(R, xmin, xmax, ymin, ymax, delta, depth, leaf_path, K, transform):
    x, y = np.arange(xmin, xmax, delta), np.arange(ymin, ymax, delta)
    X, Y = np.meshgrid(x, y)
    points = np.zeros((X[:, 0].size, X[0, :].size, 2))
    points[:, :, 0] = X
    points[:, :, 1] = Y
    colors = np.zeros((X[:, 0].size, X[0, :].size, K))

    for rows in range(X[:, 0].size):
        for cols in range(X[0, :].size):
            og_pt = points[rows, cols, :]

            #Transform from real space to inferred space
            pts = np.linalg.solve(transform[:,:-1],og_pt-transform[:,-1])
            #Compute log of probabilities
            log_prior_prob = utils.compute_leaf_log_prob(R, pts, K, depth, leaf_path)
            p_unnorm = np.exp(log_prior_prob - np.max(log_prior_prob))
            p_norm = p_unnorm / np.sum(p_unnorm)
            colors[rows, cols, :] = np.array(p_norm).flatten()
    return x, y, colors


def vector_field(A, B, R, xmin, xmax, ymin, ymax, delta, depth, leaf_path, leaf_nodes, K):
    x, y = np.arange(xmin,xmax, delta), np.arange(ymin,ymax, delta)
    X,Y = np.meshgrid(x,y)
    points = np.zeros( (X[:,0].size, X[0,:].size, 2) )
    points[:,:,0] = X
    points[:,:, 1] = Y
    arrows = np.zeros( points.shape )

    for rows in range( X[:,0].size):
        for cols in range( X[0,:].size):
            pts = points[rows, cols, :].T

            #Compute log of probabilities
            log_prior_prob = utils.compute_leaf_log_prob(R, pts, K, depth, leaf_path)
            p_unnorm = np.exp( log_prior_prob - np.max(log_prior_prob) )
            p_norm = p_unnorm / np.sum(p_unnorm)

            arrow = 0
            for k in range(K):
                arrow += p_norm[k] *(Aleaf[:, :-1, k] @ pts[:, na] )
            for k in range(K):
                arrow += np.array( p_norm[k][0]*( np.matrix(Aleaf[:,:,k])*pts + np.matrix(Bleaf[:,k]).T ) ).flatten()

            arrows[rows, cols, :] = arrow-np.array(pts).flatten()

    return x,y, arrows