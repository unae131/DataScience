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

fillRatingMatrix(ratingMatrix, binaryMatrix, theta = 0.9):
als(binaryMatrix, r_lambda = 10, nFactor = 100, alpha = 40, epoch = 10, verbose = 0):
u1 loss: 229657.15083743
data-2/u1.base 234.77228903770447 초
# 1 rmse: 1.2720455966670376

-------

fillRatingMatrix(ratingMatrix, binaryMatrix, theta = 0.9):
als(binaryMatrix, r_lambda = 20, nFactor = 100, alpha = 40, epoch = 15, verbose = 1):
loss: 329966.6665252407
data-2/u1.base 306.8446559906006 초
# 1 rmse: 1.2720455966670376
diffsum = 32362

-------

# svd

data-2/u1.base 7.456701993942261 초
diffsum = 32362
rmse: 1.2720455966670376

data-2/u2.base 7.697673082351685 초
diffSum 31469
rmse: 1.2543723530116566

data-2/u3.base 7.82302188873291 초
diffSum 30223
rmse 1.229288412049833

data-2/u4.base 7.721647262573242 초
diffSum 30233
rmse 1.2294917649175208

data-2/u5.base 7.758139133453369 초
diffSum 30501
rmse 1.2349291477651663

-------

svd

theta = 0.8
minInterest = interest[int(0.95 * len(interest))]
maxUninterest = interest[int(theta * len(interest))]
midUninterest = interest[int(0.1 * len(interest))]
            
if binaryMatrix[i][j] > minInterest:
    ratingMatrix[i][j] = 4

elif binaryMatrix[i][j] > maxUninterest:
    ratingMatrix[i][j] = 3

elif binaryMatrix[i][j] > midUninterest:
    ratingMatrix[i][j] = 2

else:
    ratingMatrix[i][j] = 1

# 1  rmse: 1.2435031162003576
# 2  rmse: 1.2192415675328658
# 3  rmse: 1.2088217403736583
# 4  rmse: 1.2115898645994032
# 5  rmse: 1.216038650701531
전체 rmse 1.219901635378853

------

theta = 0.5
minInterest = interest[int(0.9 * len(interest))]
maxUninterest = interest[int(theta * len(interest))]
midUninterest = interest[int(0.1 * len(interest))]
# 1  rmse: 1.2435031162003576
# 2  rmse: 1.2192415675328658
# 3  rmse: 1.2088217403736583
# 4  rmse: 1.2115898645994032
# 5  rmse: 1.216038650701531
전체 rmse 1.219901635378853

------

theta = 0.8
maxInterest = interest[-nUsers]
minInterest = interest[int(0.9 * len(interest))]
maxUninterest = interest[int(theta * len(interest))]
midUninterest = interest[int(0.1 * len(interest))]

if binaryMatrix[i][j] > maxInterest:
    ratingMatrix[i][j] = 5

# 1  rmse: 1.2656816345353203
# 2  rmse: 1.2412896519346321
# 3  rmse: 1.2316046443562967
# 4  rmse: 1.2344634461983879
# 5  rmse: 1.2382043450093365
전체 rmse 1.2423083353177664

-------

maxInterest 제거
minInterest = interest[int(0.95 * len(interest))]
maxUninterest = interest[int(theta * len(interest))]
midUninterest = interest[int(0.05 * len(interest))]
# 1  rmse: 1.2435031162003576
# 2  rmse: 1.2192415675328658
# 3  rmse: 1.2088217403736583
# 4  rmse: 1.2115898645994032
# 5  rmse: 1.216038650701531
전체 rmse 1.219901635378853

-------
test file 읽지 않고 예측
# 1  rmse: 1.6514236282674413
# 2  rmse: 1.5988276955319483
# 3  rmse: 1.6724383396705542
# 4  rmse: 1.6609184206335963
# 5  rmse: 1.837212562552303
전체 rmse 1.6860901518009055

------
svd
전부 2일때
# 1  rmse: 1.921119465311827
# 2  rmse: 1.9137528576072722
# 3  rmse: 1.8870744553408592
# 4  rmse: 1.8857094155781267
# 5  rmse: 1.8896163631806324
전체 rmse 1.8995130955063195

--------
svd
[2, 3] theta = 0.5
# 1  rmse: 1.5727682601069999
# 2  rmse: 1.5369287556682647
# 3  rmse: 1.5914615923735012
# 4  rmse: 1.5689964945786208
# 5  rmse: 1.5349429956842047
전체 rmse 1.5611726361937044
---------
svd
theta = 0.9
# 1  rmse: 1.7151822060644168
# 2  rmse: 1.6580259346584418
# 3  rmse: 1.731790980459247
# 4  rmse: 1.7225707532638537
# 5  rmse: 1.660813053898602
전체 rmse 1.6979723201513033
---------
svd
theta = 0.2
# 1  rmse: 1.4986493919526342
# 2  rmse: 1.4808612359029458
# 3  rmse: 1.5005998800479758
# 4  rmse: 1.4761097520171054
# 5  rmse: 1.4611981385151023
전체 rmse 1.483556537513822

theta = 0.1
# 1  rmse: 1.4409024949662625
# 2  rmse: 1.4349390230947099
# 3  rmse: 1.4308563869235793
# 4  rmse: 1.4056671014148407
# 5  rmse: 1.4051512374118311
전체 rmse 1.4235835065074336

theta = 0.05
rmse 1.3553597308463905
# 1  rmse: 1.3886504239728585
# 2  rmse: 1.3855684753919597
# 3  rmse: 1.3703649149040558
# 4  rmse: 1.353957163281025
# 5  rmse: 1.3553597308463905
전체 rmse 1.3708573959387607

theta = 0.01
# 1  rmse: 1.3081093226485314
# 2  rmse: 1.3041472309520885
# 3  rmse: 1.280234353546256
# 4  rmse: 1.2729296916954997
# 5  rmse: 1.2793162236132238
전체 rmse 1.2890267646561882

전부 3으로 예측
# 1  rmse: 1.2720455966670376
# 2  rmse: 1.2543723530116566
# 3  rmse: 1.229288412049833
# 4  rmse: 1.2294917649175208
# 5  rmse: 1.2349291477651663
전체 rmse 1.244138255982831


0.9999~ [4]
0.01~ [3]
0.0001~ [2]
# 1  rmse: 1.276146543309192
# 2  rmse: 1.2633091466462198
# 3  rmse: 1.2392134602238631
# 4  rmse: 1.2358600244364246
# 5  rmse: 1.2435031162003576
전체 rmse 1.251702840134191
--------
svd
theta = 0.1, [1~3]
maxUninterest = interest[int(theta * len(interest))]
midUninterest = interest[int(0.001 * len(interest))]
# 1  rmse: 1.4478950238190613
# 2  rmse: 1.448033148791836
# 3  rmse: 1.4452854389358525
# 4  rmse: 1.4161920773680383
# 5  rmse: 1.4177270541257228
전체 rmse 1.435102783775434