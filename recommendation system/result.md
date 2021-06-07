als(r_lambda = 40, nFactor = 100, alpha = 40, epoch = 11)
1~5 평균 rmse: 1.2501599897613105

-------

als(binaryMatrix, r_lambda = 150, nFactor = 50, alpha = 40, epoch = 10)
data-2/u5.base 172.7817211151123 초
# 1  rmse: 1.79215
# 2  rmse: 1.7521
# 3  rmse: 1.6851
# 4  rmse: 1.68045
# 5  rmse: 1.69565
전체 rmse 1.311903197648363

-------

np.svd 사용
data-2/u1.base 4.142937183380127 초
data-2/u2.base 3.996979236602783 초
data-2/u3.base 3.919766902923584 초
data-2/u4.base 3.935257911682129 초
data-2/u5.base 3.9722189903259277 초
# 1  rmse: 1.2720455966670376
# 2  rmse: 1.2543723530116566
# 3  rmse: 1.229288412049833
# 4  rmse: 1.2294917649175208
# 5  rmse: 1.2349291477651663
전체 rmse 1.244138255982831

-------

fillRatingMatrix(ratingMatrix, binaryMatrix, theta = 0.5)
als(binaryMatrix, r_lambda = 150, nFactor = 100, alpha = 40, epoch = 10)
data-2/u5.base 217.95952200889587 초
# 1  rmse: 1.3409325113517085
# 2  rmse: 1.269232051281404
# 3  rmse: 1.2443271274066157
# 4  rmse: 1.2439654336033619
# 5  rmse: 1.2505598746161657
전체 rmse 1.27033460159125

-------

fillRatingMatrix(ratingMatrix, binaryMatrix, theta = 0.5):
als(binaryMatrix, r_lambda = 20, nFactor = 100, alpha = 40, epoch = 10)
np.random.rand(nUsers, nFactor) * 0.16
data-2/u5.base 221.7027130126953 초
# 1  rmse: 1.2720455966670376
# 2  rmse: 1.2543723530116566
# 3  rmse: 1.229288412049833
# 4  rmse: 1.2294917649175208
# 5  rmse: 1.2349291477651663
전체 rmse 1.244138255982831

-------

als(binaryMatrix, r_lambda = 10, nFactor = 100, alpha = 40, epoch = 10, verbose = 0):
u1 loss: 229657.15083743
data-2/u1.base 234.77228903770447 초
# 1 rmse: 1.2720455966670376
