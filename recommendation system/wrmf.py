import numpy as np

class WRMF():
    def als(binaryMatrix, r_lambda = 20, nFactor = 100, alpha = 40, epoch = 10, verbose = 1):
        nUsers = len(binaryMatrix)
        nItems = len(binaryMatrix[0])

        # initialize U and V
        U = np.random.rand(nUsers, nFactor) * 0.16
        V = np.random.rand(nItems, nFactor) * 0.16
        C = 1 + alpha * binaryMatrix

        # loss
        for k in range(epoch):
            if verbose > 0:
                print("(" + str(k+1) +"/"+str(epoch) + ")", "loss:", WRMF.__loss(binaryMatrix, U, V, C, r_lambda))

            U, V = WRMF.__update(binaryMatrix, nUsers, nItems, nFactor, U, V, C, r_lambda)
        
        finalLoss = WRMF.__loss(binaryMatrix, U, V, C, r_lambda)
        
        print("loss:",finalLoss)

        return U @ V.T, finalLoss, U, V

    def __loss(binaryMatrix, U, V, C, r_lambda):
        return np.sum(C * (binaryMatrix - (U @ V.T) ** 2)) + r_lambda * (np.sum(U*U) + np.sum(V*V)) 

    def __update(binaryMatrix, nUsers, nItems, nFactor, U, V, C, r_lambda):
        lambdaI = r_lambda * np.eye(nFactor)

        for u in range(nUsers):
            Cu = np.diag(C[u])
            U[u] = np.linalg.inv(V.T @ Cu @ V + lambdaI) @ V.T @ Cu @ binaryMatrix[u]

        for i in range(nItems):
            Ci = np.diag(C[:, i])
            V[i] = np.linalg.inv(U.T @ Ci @ U + lambdaI) @ U.T @ Ci @ binaryMatrix[:, i]

        return U, V