import numpy as np

image_to_arm = np.load("image_to_arm.npy")
arm_to_image = np.load("arm_to_image.npy")

centers = np.loadtxt("centers.txt")
real_points = np.loadtxt("real_points.txt")

tranformed = np.dot(image_to_arm,centers.T).T
tranformed = tranformed[:, :-1]

arms = real_points[:,:-1]

# 打印结果
##print(tranformed)
#print(real_points)

cs = np.array([[ 165.25210568,  141.00335488, -178.54518478,1.],
    [ 157.01899904,  111.43952695, -176.31177964, 1.],
    [ 168.08157029,   87.78031634, -181.0908021 ,    1. ],
    [ 187.61739247,   60.4848038 , -186.57355584,    1. ],
    [ 175.00610081,   35.67979156, -183.20441345,    1.],
    [ 177.6946931 ,   -8.49344957, -183.42189609,    1.],
    [ 185.70198661,  -23.21297015, -184.08540324,    1. ],
    [ 197.04766126,  -50.19693849, -193.52285073,    1.],])

imgcenter = np.array([[-0.172117, -0.241227, 0.505000, 1.000000],
[-0.093457, -0.189007, 0.500000, 1.000000],
[-0.002655, -0.174039, 0.506000, 1.000000],
[-0.005685, -0.124534, 0.492000, 1.000000],
[-0.115161, -0.155263, 0.493000, 1.000000],
[-0.200919, -0.208144, 0.499000, 1.000000],
[-0.208892, -0.184737, 0.497000, 1.000000],])

origin = np.dot(np.linalg.inv(image_to_arm),cs.T)
to = origin.T
to[:,2] = to[:,2] - 0.2
to = to.T
print(to[:,2])

transforms = np.dot(image_to_arm,to).T
print(origin.T)
print(transforms)
# 将去掉最后一列后的 transformed 保存到 CSV 文件
#np.savetxt("transform.csv", tranformed, delimiter=",")
#np.savetxt("arm_points.csv", arms, delimiter=",")