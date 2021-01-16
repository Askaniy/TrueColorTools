
# Reflectivity measurements by wavelengths

objects = {
    #"Zero Mag": {"filters": "Landolt", "indices": {"U-B": 0, "B-V": 0, "V-R": 0, "R-I": 0}},
    "Vega|1": {
        "nm": list(range(100, 1005, 5)),
        "br": [6e-05, 0.00025, 0.00576, 0.03232, 0.00055, 0.08193, 0.63839, 1.10497, 1.31761, 1.49697, 1.59407, 1.56707, 1.62778, 1.52787, 1.48626, 1.4522, 
        1.47706, 1.37099, 1.36909, 1.35627, 1.2874, 1.23782, 1.2184, 1.12704, 1.10038, 1.03818, 1.02341, 0.93665, 0.89169, 0.89966, 0.89559, 0.84866, 
        0.87022, 0.89975, 0.86962, 0.83412, 0.8045, 0.82241, 0.83534, 0.82666, 0.83803, 0.82499, 0.80312, 0.7947, 0.77471, 0.76373, 0.76404, 0.74179, 
        0.73851, 0.73079, 0.71667, 0.71153, 0.69922, 0.69187, 0.70452, 0.87057, 1.27801, 1.47797, 1.49367, 1.54471, 1.81878, 1.91241, 1.2929, 1.79114, 
        1.77413, 1.70716, 1.56168, 1.11728, 1.52847, 1.50317, 1.44746, 1.4018, 1.36738, 1.32857, 1.28946, 1.24422, 1.18237, 0.85037, 1.06147, 1.09692, 
        1.06894, 1.03883, 1.01305, 0.97619, 0.94761, 0.92189, 0.89605, 0.87237, 0.84757, 0.82806, 0.80377, 0.78387, 0.76136, 0.74286, 0.72311, 0.7045, 
        0.68684, 0.66853, 0.64976, 0.63457, 0.61812, 0.60278, 0.58685, 0.57205, 0.55971, 0.54451, 0.53353, 0.51601, 0.50537, 0.49307, 0.47527, 0.37761, 
        0.43725, 0.44816, 0.4396, 0.42995, 0.42074, 0.41263, 0.40258, 0.39369, 0.38466, 0.37642, 0.36723, 0.35911, 0.35233, 0.34516, 0.33668, 0.33015, 
        0.32281, 0.31598, 0.30998, 0.30301, 0.29675, 0.29095, 0.28478, 0.27771, 0.27262, 0.26772, 0.2627, 0.25759, 0.25282, 0.24721, 0.24302, 0.2378, 
        0.2323, 0.22828, 0.22451, 0.22018, 0.21685, 0.21096, 0.20805, 0.20542, 0.20146, 0.19538, 0.20773, 0.18605, 0.20945, 0.17968, 0.19996, 0.20476, 
        0.17369, 0.18799, 0.19469, 0.19582, 0.17148, 0.16286, 0.18356, 0.18016, 0.17867, 0.17445, 0.16444, 0.13792, 0.16047, 0.16176, 0.16256, 0.15818, 
        0.15698, 0.1527, 0.15107, 0.14542, 0.13953],
        "obl": 0.161817 # https://iopscience.iop.org/article/10.1088/0004-637X/708/1/71
    },
    "Sun|1": {
        "nm": list(range(200, 1005, 5)),
        "br": [0.0014, 0.01011, 0.02381, 0.03433, 0.04319, 0.0517, 0.04901, 0.04446, 0.04279, 0.055, 0.05044, 0.07057, 0.09784, 0.22107, 0.23546, 0.18081, 
        0.13324, 0.24966, 0.47614, 0.50681, 0.44031, 0.57326, 0.59473, 0.63443, 0.69563, 0.79136, 0.95555, 0.87621, 0.91949, 0.87208, 0.92131, 0.98853, 
        0.85355, 1.06107, 1.12238, 0.95982, 1.12773, 0.88242, 1.14262, 0.91021, 1.59446, 1.59842, 1.60575, 1.64867, 1.61866, 1.60261, 1.37227, 1.64495, 
        1.64123, 1.77152, 1.92485, 1.87994, 1.88343, 1.8611, 1.83783, 1.86924, 1.91484, 1.73616, 1.8141, 1.84016, 1.75081, 1.80945, 1.81457, 1.70382, 
        1.68404, 1.73918, 1.80316, 1.78269, 1.72313, 1.75849, 1.74756, 1.74919, 1.69428, 1.71289, 1.69428, 1.73081, 1.70358, 1.7101, 1.62401, 1.66961, 
        1.63937, 1.65309, 1.6175, 1.56678, 1.59865, 1.55119, 1.55886, 1.54397, 1.50582, 1.50675, 1.49837, 1.36063, 1.4658, 1.44393, 1.41461, 1.4081, 
        1.39228, 1.36342, 1.35133, 1.33085, 1.29362, 1.31363, 1.29269, 1.26896, 1.24151, 1.25733, 1.23685, 1.2201, 1.17357, 1.19497, 1.17729, 1.16752, 
        1.15403, 1.12238, 1.12331, 1.11215, 1.10749, 1.09958, 1.0805, 1.06654, 1.06561, 1.04281, 1.03955, 1.03164, 1.00791, 1.00372, 0.99581, 0.98046, 
        0.97348, 0.95859, 0.93439, 0.87948, 0.9288, 0.8618, 0.89018, 0.89158, 0.86459, 0.85807, 0.85202, 0.85528, 0.82829, 0.81992, 0.80875, 0.80037, 
        0.77385, 0.78083, 0.78548, 0.76315, 0.7571, 0.76035, 0.74407, 0.7436, 0.73145, 0.71822, 0.7206, 0.71192, 0.70569, 0.69804, 0.6884, 0.68677, 
        0.68053],
        "obl": 9e-6
    },
    "Mercury|2": {
        "nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.087, 0.105, 0.142, 0.158, 0.172, 0.180, 0.208], "albedo": True
    },
    #"Mercury|3": {
    #    "nm": [314.7, 359.0, 392.6, 415.5, 457.5, 501.2, 626.4, 729.7, 959.5, 1063.5], "br": [0.61, 0.56, 0.66, 0.71, 0.86, 1.00, 1.37, 1.50, 1.77, 2.01],
    #    "albedo": 0.142
    #},
    "Venus|2": {
        "nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.348, 0.658, 0.689, 0.658, 0.708, 0.640, 0.584], "albedo": True
    },
    #"Venus|3": {
    #    "nm": [314.7, 359.0, 392.6, 415.5, 457.5, 501.2, 626.4, 729.7, 959.5, 1063.5], "br": [0.59, 0.64, 0.72, 0.58, 0.95, 1.00, 1.16, 1.08, 1.16, 1.12],
    #    "albedo": 0.689
    #},
    #"Earth|2": {
    #    "nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.688, 0.512, 0.434, 0.392, 0.418, 0.396, 0.430], "albedo": True, "obl": 0.0033528
    #},
    "Earth|3": {
        "nm": [350, 450, 550, 650, 750, 850, 950], "br": [1610.47, 1342.71, 1059.02, 1014.27, 1062.25, 1168.00, 853.79], "albedo": 0.434, "obl": 0.0033528
    },
    "Moon|3": {"nm": [350, 450, 550, 650, 750, 850, 950], "br": [13.83, 18.06, 22.54, 26.68, 30.74, 34.86, 34.14], "obl": 0.001438435},
    #"Mars|2": {"nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.060, 0.088, 0.170, 0.250, 0.288, 0.285, 0.330], "albedo": 0.170, "obl": 0.005886},
    #"Mars|3": {"nm": [350, 450, 550, 650, 750, 850, 950], "br": [4.52, 6.87, 13.09, 21.60, 25.32, 26.55, 24.31], "albedo": 0.170, "obl": 0.005886},
    "Mars:B|4": {
        "nm": [330, 342, 363, 381, 404, 440, 475, 504, 540, 566, 600, 633, 666, 700, 704.7, 716.4, 728.9, 739.8, 751.9, 763.6, 775.6, 786.3, 799, 811.7,
        822.4, 837.1, 849.8, 862.5],
        "br": [0.091700, 0.095981, 0.108666, 0.098961, 0.130791, 0.180553, 0.247580, 0.302547, 0.398298, 0.527668, 0.704229, 0.790133, 0.861244, 0.907984,
        0.927670, 0.950918, 0.968006, 0.973932, 1.007903, 1.009743, 0.983539, 0.998712, 1.002135, 0.990941, 0.984577, 0.981692, 0.969340, 0.963597],
        "albedo": 0.26, "obl": 0.005886 # albedo https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2001JE001580
    },
    "Mars:D|4": {
        "nm": [330, 342, 363, 381, 404, 440, 475, 504, 540, 566, 600, 633, 644.1, 656, 667.9, 679.9, 691.7, 704.7, 716.4, 728.9, 739.8, 751.9, 763.6,
        775.6, 786.3, 799, 811.7, 822.4, 837.1, 849.8, 862.5],
        "br": [0.214259, 0.225981, 0.208343, 0.207151, 0.242350, 0.304599, 0.368299, 0.435753, 0.552943, 0.686686, 0.832221, 0.931029, 1.086725, 1.096983, 
        1.117898, 1.128430, 1.139110, 1.147979, 1.159085, 1.143423, 1.145229, 1.126660, 1.111953, 1.092715, 1.076242, 1.085038, 1.046774, 1.033783,
        1.026548, 1.020545, 1.028644],
        "albedo": 0.12, "obl": 0.005886 # albedo https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2001JE001580
    },
    #"Jupiter|2": {"nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.358, 0.443, 0.538, 0.513, 0.495, 0.389, 0.321], "obl": 0.06487},
    #"Jupiter|3": {"nm": [350, 450, 550, 650, 750, 850], "br": [0.604, 0.824, 1.000, 1.006, 0.832, 0.636], "obl": 0.06487},
    "Jupiter|5": {
        "nm": list(range(300, 1000, 5)),
        "br": [0.29378, 0.28429, 0.27608, 0.27136, 0.27249, 0.27212, 0.27459, 0.28014, 0.28171, 0.28694, 0.29027, 0.29465, 0.30181, 0.30318, 0.30942, 
        0.31845, 0.32228, 0.32985, 0.33479, 0.3483, 0.34522, 0.35446, 0.36173, 0.3716, 0.38007, 0.38811, 0.39714, 0.40009, 0.40802, 0.4144, 0.42059, 
        0.42694, 0.43275, 0.43956, 0.44462, 0.44928, 0.45416, 0.45455, 0.4655, 0.47041, 0.47498, 0.4778, 0.48142, 0.48899, 0.49216, 0.49489, 0.49725, 
        0.4985, 0.48837, 0.49256, 0.50378, 0.50928, 0.51787, 0.52036, 0.51759, 0.51445, 0.52115, 0.52432, 0.52029, 0.51862, 0.52119, 0.52058, 0.51544, 
        0.47293, 0.43412, 0.49536, 0.51866, 0.52015, 0.51493, 0.48642, 0.49555, 0.50965, 0.50992, 0.5037, 0.50962, 0.52745, 0.52588, 0.51956, 0.52132, 
        0.50772, 0.47595, 0.4699, 0.49182, 0.47992, 0.36248, 0.24382, 0.27116, 0.39441, 0.47938, 0.50638, 0.50398, 0.49315, 0.46238, 0.45192, 0.45735, 
        0.44768, 0.40332, 0.33954, 0.33709, 0.3421, 0.36213, 0.40581, 0.43052, 0.44705, 0.46682, 0.47588, 0.4809, 0.44709, 0.38267, 0.41849, 0.43172, 
        0.35489, 0.22159, 0.18372, 0.27352, 0.32265, 0.17022, 0.04325, 0.04078, 0.04605, 0.09136, 0.22011, 0.33562, 0.35873, 0.39662, 0.39147, 0.39727, 
        0.41455, 0.4393, 0.44514, 0.42942, 0.43015, 0.37152, 0.23525, 0.18172, 0.18811, 0.15767, 0.10329, 0.07357, 0.08545],
        "albedo": True, "obl": 0.06487
    },
    "Io:T|4": {
        "nm": [350, 375, 400, 433, 466, 500, 533, 566, 600, 633, 666, 700, 733, 739.8, 751.9, 763.6, 775.6, 786.3, 799, 811.7, 822.4, 837.1, 849.8, 862.5],
        "br": [0.126856, 0.161157, 0.189998, 0.312668, 0.455349, 0.642046, 0.775382, 0.801427, 0.811630, 0.890139, 0.942953, 1.004252, 1.005697, 1.015561,
        1.031987, 1.019722, 1.008961, 1.000501, 1.015732, 1.006328, 1.003697, 0.986871, 0.973683, 0.987817]
    },
    "Europa:T|4": {
        "nm": [350, 375, 400, 433, 466, 500, 533, 566, 600, 633, 666, 700, 733, 766, 800, 833, 866],
        "br": [0.352826, 0.410782, 0.467415, 0.602579, 0.688769, 0.806425, 0.839300, 0.852109, 0.913667, 0.961235, 0.979446, 1.006591, 1.026941, 1.038414,
        1.067850, 1.062889, 1.063046]
    },
    "Ganymede:L|4": {
        "nm": [350, 375, 400, 433, 466, 500, 533, 566, 600, 633, 666, 700, 733, 766, 800, 833, 866],
        "br": [0.488778, 0.590744, 0.632155, 0.752500, 0.783059, 0.869610, 0.918507, 0.955278, 0.973874, 1.010833, 1.021557, 1.046712, 1.040900, 1.035977,
        1.049606, 1.044146, 1.036557]
    },
    "Callisto:L|4": {
        "nm": [350, 375, 400, 433, 466, 500, 533, 566, 600, 633, 666, 700, 733, 766, 800, 833, 837.1, 849.8, 862.5],
        "br": [0.406242, 0.456089, 0.518130, 0.652152, 0.691349, 0.777651, 0.840575, 0.881522, 0.918704, 0.941487, 0.969265, 0.990831, 0.997041, 0.993501,
        1.007422, 0.986979, 1.001239, 0.985442, 1.006188]
    },
    #"Saturn|2": {"nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.203, 0.339, 0.499, 0.646, 0.568, 0.543, 0.423], "obl": 0.09796},
    #"Saturn|3": {"nm": [350, 450, 550, 650, 750, 850], "br": [0.445, 0.684, 1.000, 1.144, 1.001, 0.776], "obl": 0.09796},
    "Saturn|5": {
        "nm": list(range(300, 1000, 5)),
        "br": [0.25845, 0.25605, 0.24952, 0.23874, 0.23387, 0.22685, 0.22264, 0.21964, 0.21405, 0.21096, 0.20684, 0.20468, 0.20455, 0.20151, 0.20191, 
        0.20496, 0.20594, 0.20962, 0.21328, 0.22295, 0.22405, 0.23403, 0.24293, 0.25509, 0.26686, 0.27894, 0.29168, 0.30152, 0.31439, 0.32584, 0.33679, 
        0.34745, 0.35724, 0.36685, 0.3755, 0.38363, 0.39057, 0.39448, 0.40676, 0.41362, 0.42072, 0.42719, 0.43207, 0.4407, 0.44692, 0.45191, 0.45758, 
        0.46124, 0.45336, 0.46074, 0.4799, 0.48627, 0.4955, 0.50115, 0.50336, 0.50165, 0.51342, 0.52293, 0.52792, 0.52662, 0.53269, 0.53723, 0.5297, 
        0.47745, 0.43003, 0.52021, 0.5551, 0.55935, 0.55703, 0.54683, 0.55186, 0.55582, 0.5521, 0.54076, 0.55193, 0.58783, 0.58702, 0.57692, 0.58883, 
        0.57394, 0.52331, 0.51846, 0.5558, 0.53638, 0.3774, 0.24997, 0.28012, 0.42615, 0.54086, 0.58456, 0.58327, 0.57626, 0.55067, 0.53454, 0.53422, 
        0.50875, 0.45304, 0.42209, 0.44639, 0.39987, 0.39828, 0.45145, 0.49315, 0.52884, 0.55152, 0.56146, 0.56964, 0.52177, 0.42206, 0.47465, 0.50051, 
        0.40093, 0.25017, 0.19992, 0.316, 0.37931, 0.22795, 0.05283, 0.04931, 0.05245, 0.11242, 0.27285, 0.39963, 0.40986, 0.47555, 0.51275, 0.53154, 
        0.54184, 0.54968, 0.52981, 0.50034, 0.50075, 0.43722, 0.27446, 0.22052, 0.24216, 0.22974, 0.13768, 0.10328, 0.12643],
        "albedo": True, "obl": 0.09796
    },
    "Rings|4": {
        "nm": [326, 343, 360, 383, 403, 435, 469, 500, 534, 566, 599, 633, 644.1, 656, 667.9, 679.9, 691.7, 704.7, 716.4, 728.9, 739.8, 751.9, 763.6,
        775.6, 786.3, 799, 811.7, 822.4, 837.1, 849.8, 862.5],
        "br": [0.3132, 0.3528, 0.3933, 0.4455, 0.5112, 0.5886, 0.6966, 0.7686, 0.8604, 0.9000, 0.9234, 0.9612, 1.081513, 1.065072, 1.088894, 1.094878,
        1.092790, 1.097008, 1.098860, 1.088170, 1.079328, 1.086258, 1.092842, 1.072758, 1.064449, 1.052381, 1.049213, 1.039174, 1.038871, 1.028878,
        1.016596], "obl": 0.5
    },
    "Rhea|4": {
        "nm": [325, 350, 375, 400, 433, 466, 500, 533, 566, 600, 633, 666, 700, 733, 766, 800, 833, 866],
        "br": [0.734770, 0.732256, 0.745028, 0.844831, 0.859745, 0.910340, 0.925726, 0.991097, 0.992538, 1.016375, 1.006958, 1.049296, 1.060323, 1.034402,
        1.082394, 1.054788, 1.060017, 1.028328]
    },
    #"Titan|3": {"nm": [350, 450, 550, 650, 750, 850], "br": [0.344, 0.584, 1.000, 1.248, 1.101, 0.879]},
    "Titan|5": {
        "nm": list(range(300, 1000, 5)),
        "br": [0.06505, 0.05856, 0.05638, 0.05807, 0.0603, 0.06186, 0.06338, 0.06517, 0.06666, 0.06874, 0.07017, 0.07212, 0.07408, 0.07608, 0.07853, 
        0.0811, 0.0835, 0.08513, 0.08827, 0.09123, 0.09332, 0.09631, 0.09867, 0.1027, 0.10647, 0.10989, 0.11321, 0.11655, 0.12048, 0.12456, 0.12877, 
        0.13279, 0.13668, 0.14085, 0.14481, 0.14926, 0.15348, 0.15718, 0.1631, 0.16837, 0.17338, 0.17853, 0.18298, 0.1886, 0.19378, 0.1979, 0.20247, 
        0.20686, 0.20645, 0.21208, 0.22318, 0.22765, 0.23281, 0.23653, 0.23968, 0.23997, 0.24713, 0.25345, 0.25808, 0.25722, 0.26167, 0.26689, 0.26162, 
        0.23905, 0.22615, 0.2607, 0.28117, 0.28428, 0.2838, 0.28511, 0.28383, 0.27784, 0.27137, 0.26361, 0.26989, 0.29295, 0.29239, 0.28499, 0.29349, 
        0.28642, 0.25493, 0.25172, 0.27407, 0.26432, 0.20588, 0.17638, 0.18245, 0.216, 0.26529, 0.29712, 0.29887, 0.30022, 0.27882, 0.25866, 0.25792, 
        0.23868, 0.21503, 0.20469, 0.21106, 0.19575, 0.19417, 0.20825, 0.22757, 0.26836, 0.29139, 0.30378, 0.30712, 0.24885, 0.19112, 0.2104, 0.22228, 
        0.18074, 0.14396, 0.13371, 0.15669, 0.16882, 0.12871, 0.08855, 0.08504, 0.08617, 0.10392, 0.13792, 0.16482, 0.16551, 0.18738, 0.21539, 0.24828, 
        0.27305, 0.27734, 0.22799, 0.19868, 0.19731, 0.16681, 0.12782, 0.11507, 0.11953, 0.11382, 0.09641, 0.08534, 0.08749],
		"albedo": True
    },
    #"Uranus|2": {"nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.502, 0.561, 0.488, 0.264, 0.202, 0.089, 0.079], "obl": 0.02293},
    #"Uranus|3": {"nm": [350, 450, 550, 650, 750, 850], "br": [0.984, 1.067, 1.000, 0.647, 0.292, 0.148], "obl": 0.02293},
    "Uranus|5": {
        "nm": list(range(300, 1000, 5)),
        "br": [0.53, 0.52915, 0.53383, 0.52396, 0.52481, 0.51762, 0.51994, 0.53179, 0.51993, 0.52475, 0.51689, 0.51507, 0.52749, 0.51285, 0.52179, 0.53988, 
        0.53582, 0.5555, 0.53676, 0.57531, 0.52632, 0.53684, 0.54856, 0.55668, 0.56234, 0.57533, 0.5903, 0.57235, 0.55516, 0.58489, 0.58799, 0.58555, 
        0.57635, 0.60338, 0.61043, 0.60925, 0.56945, 0.49064, 0.61783, 0.62374, 0.62342, 0.58807, 0.53888, 0.63396, 0.60169, 0.6039, 0.60351, 0.51239, 
        0.3696, 0.39366, 0.61272, 0.59345, 0.60032, 0.57245, 0.49374, 0.41179, 0.47933, 0.58708, 0.55863, 0.43903, 0.45503, 0.49154, 0.36375, 0.2004, 
        0.14279, 0.29586, 0.4688, 0.48747, 0.43639, 0.41545, 0.38462, 0.32972, 0.282, 0.23652, 0.25987, 0.3904, 0.37752, 0.3196, 0.36736, 0.31736, 0.17937, 
        0.16727, 0.24258, 0.20607, 0.06851, 0.05045, 0.05197, 0.08079, 0.20042, 0.32091, 0.32824, 0.32625, 0.24262, 0.17686, 0.17233, 0.12197, 0.07435, 
        0.05988, 0.06677, 0.04694, 0.05014, 0.06658, 0.09073, 0.12937, 0.19451, 0.19966, 0.25324, 0.1432, 0.04888, 0.07196, 0.08931, 0.04316, 0.02682, 
        0.02329, 0.02965, 0.03571, 0.02553, 0.01525, 0.01617, 0.01632, 0.01784, 0.02397, 0.03561, 0.03616, 0.06612, 0.11919, 0.19142, 0.2696, 0.26834, 
        0.15181, 0.09542, 0.08876, 0.04618, 0.01896, 0.01611, 0.01781, 0.01818, 0.01391, 0.01367, 0.01475],
        "albedo": True, "obl": 0.02293
    },
    #"Neptune|2": {"nm": [360, 436, 549, 641, 700, 798, 900], "br": [0.578, 0.562, 0.442, 0.226, 0.181, 0.072, 0.067], "obl": 0.0171},
    #"Neptune|3": {"nm": [350, 450, 550, 650, 750, 850], "br": [1.252, 1.235, 1.000, 0.555, 0.237, 0.132], "obl": 0.0171},
    "Neptune|5": {
        "nm": list(range(300, 1000, 5)),
        "br": [0.55168, 0.57462, 0.5749, 0.56581, 0.56727, 0.55883, 0.56295, 0.5772, 0.56453, 0.5712, 0.56445, 0.56291, 0.57946, 0.5619, 0.57126, 0.59178, 
        0.58364, 0.60495, 0.57921, 0.62125, 0.56071, 0.56722, 0.57935, 0.58255, 0.58109, 0.59381, 0.60457, 0.57878, 0.54865, 0.58534, 0.5848, 0.57342, 
        0.55558, 0.58414, 0.58875, 0.58025, 0.52666, 0.43538, 0.57688, 0.58207, 0.5751, 0.52714, 0.47207, 0.5743, 0.5355, 0.54054, 0.5359, 0.43401, 
        0.29436, 0.31937, 0.53876, 0.51595, 0.51995, 0.48469, 0.39902, 0.31661, 0.38518, 0.49656, 0.46291, 0.33844, 0.3543, 0.39254, 0.26611, 0.14905, 
        0.11786, 0.21077, 0.37214, 0.39651, 0.33405, 0.30996, 0.27639, 0.22648, 0.18755, 0.15644, 0.17152, 0.27978, 0.26628, 0.21377, 0.25585, 0.21215, 
        0.11902, 0.11127, 0.1541, 0.13436, 0.06525, 0.05146, 0.0533, 0.0687, 0.12779, 0.21497, 0.22218, 0.22058, 0.15187, 0.10806, 0.10511, 0.08013, 
        0.05973, 0.05367, 0.05566, 0.04579, 0.04835, 0.0544, 0.06348, 0.08654, 0.13235, 0.13991, 0.17967, 0.09125, 0.04387, 0.05283, 0.05988, 0.04176, 
        0.03146, 0.02746, 0.03408, 0.03774, 0.0298, 0.01621, 0.01774, 0.01806, 0.02114, 0.02931, 0.03572, 0.03514, 0.04545, 0.06665, 0.10763, 0.16505, 
        0.16553, 0.08372, 0.05606, 0.05255, 0.03725, 0.02468, 0.02116, 0.02346, 0.02395, 0.01784, 0.01751, 0.01883],
        "albedo": True, "obl": 0.0171
    },
    "C/1995O1-HB|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.390}, "sun": True
	},
	"C/1999J2|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.687, "V-R": 0.426, "R-I": 0.403}, "sun": True
	},
	"C/2001G1|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.752, "V-R": 0.430, "R-I": 0.433}, "sun": True
	},
	"C/2001M10|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.963, "V-R": 0.350, "R-I": 0.520}, "sun": True
	},
	"C/2002CE10-LINEA|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.542, "R-I": 0.504}, "sun": True
	},
	"C/2002VQ94-LINEA|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.500, "R-I": 0.480}, "sun": True
	},
	"C/2003A2-Gleason|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.610, "V-R": 0.470, "R-I": 0.460}, "sun": True
	},
	"C/2004D1-NEAT|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.430, "R-I": 0.510}, "sun": True
	},
	"C/2006S3-Loneos|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.580}, "sun": True
	},
	"C/2007D1-LINEAR|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.440, "R-I": 0.410}, "sun": True
	},
	"C/2008S3-Boattin|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.769, "V-R": 0.448, "R-I": 0.364}, "sun": True
	},
	"C/2009T1-McNaugh|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.640, "V-R": 0.530, "R-I": 0.450}, "sun": True
	},
	"C/2010D4-WISE|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.460}, "sun": True
	},
	"C/2010DG56-WISE|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.370}, "sun": True
	},
	"C/2010L3-Catalin|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.420, "R-I": 0.410}, "sun": True
	},
	"C/2010U3-Boattin|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.778, "V-R": 0.520, "R-I": 0.320}, "sun": True
	},
	"C/2011P2-PANSTAR|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.919, "V-R": 0.323}, "sun": True
	},
	"C/2011Q1-PANSTAR|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.819, "V-R": 0.489}, "sun": True
	},
	"C/2012A1-PANSTAR|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.450}, "sun": True
	},
	"C/2012E1-Hill|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.400}, "sun": True
	},
	"C/2012LP26-Palom|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.854, "V-R": 0.516}, "sun": True
	},
	"C/2012Q1-Kowalsk|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.907, "V-R": 0.537}, "sun": True
	},
	"C/2013C2|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.887, "V-R": 0.533}, "sun": True
	},
	"C/2013E1-McNaugh|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.480}, "sun": True
	},
	"C/2013H2-Boattin|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.490}, "sun": True
	},
	"C/2013P3-Palomar|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.450}, "sun": True
	},
	"C/2013P4|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.827, "V-R": 0.487}, "sun": True
	},
	"C/2014AA52-CATAL|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.410}, "sun": True
	},
	"C/2014B1-Schwarz|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.580}, "sun": True
	},
	"C/2014R1-Borisov|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.460}, "sun": True
	},
	"C/2014W6-Catalin|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.450}, "sun": True
	},
	"C/2014XB8-PANSTA|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.440}, "sun": True
	},
	"C/2015B1-PANSTAR|9": {"tags": ["solar_system", "minor_body", "comet", "comet-lp"],
		"filters": "Landolt", "indices": {"B-V": 0.780, "V-R": 0.450}, "sun": True
	},
	"P/2011S1-Gibbs|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.960, "V-R": 0.590}, "sun": True
	},
	"1P/Halley|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.410, "R-I": 0.390}, "sun": True
	},
	"2P/Encke|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.780, "V-R": 0.424, "R-I": 0.408}, "sun": True
	},
	"6P/dArrest|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.563, "R-I": 0.450}, "sun": True
	},
	"8P/Tuttle|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.890, "V-R": 0.530, "R-I": 0.530}, "sun": True
	},
	"10P/Tempel2|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.800, "V-R": 0.521, "R-I": 0.520}, "sun": True
	},
	"21P/GZ|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.800, "V-R": 0.500}, "sun": True
	},
	"22P/Kopff|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.795, "V-R": 0.519, "R-I": 0.450}, "sun": True
	},
	"39P/Oterma|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.890, "V-R": 0.386, "R-I": 0.412}, "sun": True
	},
	"45P/HMP|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 1.080, "V-R": 0.440, "R-I": 0.210}, "sun": True
	},
	"47P/AJ|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.780, "V-R": 0.400}, "sun": True
	},
	"49P/AR|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.471, "R-I": 0.444}, "sun": True
	},
	"55P/TT|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.510, "R-I": 0.420}, "sun": True
	},
	"86P/Wild3|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 1.580, "V-R": 0.555}, "sun": True
	},
	"106P/Schuster|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 1.010, "V-R": 0.520, "R-I": 0.450}, "sun": True
	},
	"107P/WH|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.674, "V-R": 0.361}, "sun": True
	},
	"114P/WS|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.460, "R-I": 0.540}, "sun": True
	},
	"143P/KM|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.580, "R-I": 0.560}, "sun": True
	},
	"166P/2001T4|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.870, "V-R": 0.695, "R-I": 0.735}, "sun": True
	},
	"166P/NEAT|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.890, "V-R": 0.560}, "sun": True
	},
	"167P/CINEOS|9": {"tags": ["solar_system", "minor_body", "comet", "comet-sp"],
		"filters": "Landolt", "indices": {"B-V": 0.758, "V-R": 0.516, "R-I": 0.504}, "sun": True
	},
	"1994 EV3|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.065, "V-R": 0.588, "R-I": 0.800}, "sun": True
	},
	"1994 TA|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.261, "V-R": 0.672, "R-I": 0.740}, "sun": True
	},
	"1995 HM5|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.649, "V-R": 0.460, "R-I": 0.428}, "sun": True
	},
	"1996 RQ20|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.935, "V-R": 0.558, "R-I": 0.591}, "sun": True
	},
	"1996 RR20|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.143, "V-R": 0.730, "R-I": 0.628}, "sun": True
	},
	"1996 TK66|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.993, "V-R": 0.680, "R-I": 0.551}, "sun": True
	},
	"1996 TS66|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.028, "V-R": 0.672, "R-I": 0.637}, "sun": True
	},
	"1997 QH4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.088, "V-R": 0.641, "R-I": 0.631}, "sun": True
	},
	"1998 FS144|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.950, "V-R": 0.588, "R-I": 0.510}, "sun": True
	},
	"1998 KS65|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.090, "V-R": 0.640}, "sun": True
	},
	"1998 UR43|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.784, "V-R": 0.583, "R-I": 0.354}, "sun": True
	},
	"1998 WS31|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.726, "V-R": 0.606, "R-I": 0.439}, "sun": True
	},
	"1998 WU24|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.780, "V-R": 0.530, "R-I": 0.460}, "sun": True
	},
	"1998 WV24|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.502, "R-I": 0.450}, "sun": True
	},
	"1998 WV31|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.521, "R-I": 0.481}, "sun": True
	},
	"1998 WX24|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.090, "V-R": 0.727, "R-I": 0.500}, "sun": True
	},
	"1998 WZ31|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.727, "V-R": 0.489, "R-I": 0.339}, "sun": True
	},
	"1999 CB119|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.212, "V-R": 0.714, "R-I": 0.645}, "sun": True
	},
	"1999 CX131|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.918, "V-R": 0.664, "R-I": 0.434}, "sun": True
	},
	"1999 HS11|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.121, "V-R": 0.698, "R-I": 0.600}, "sun": True
	},
	"1999 HV11|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.110, "V-R": 0.590}, "sun": True
	},
	"1999 LE31|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.748, "V-R": 0.467, "R-I": 0.521}, "sun": True
	},
	"1999 OJ4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.098, "V-R": 0.668, "R-I": 0.549}, "sun": True
	},
	"1999 RX214|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.054, "V-R": 0.593, "R-I": 0.530}, "sun": True
	},
	"1999 TR11|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.020, "V-R": 0.750, "R-I": 0.650}, "sun": True
	},
	"2000 CL104|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.223, "V-R": 0.600, "R-I": 0.612}, "sun": True
	},
	"2000 FS53|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.060, "V-R": 0.710}, "sun": True
	},
	"2000 HE46|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.870, "V-R": 0.550, "R-I": 0.400}, "sun": True
	},
	"2000 KK4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.910, "V-R": 0.580, "R-I": 0.640}, "sun": True
	},
	"2001 FM194|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.760, "V-R": 0.440}, "sun": True
	},
	"2001 KA77|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.104, "V-R": 0.704, "R-I": 0.716}, "sun": True
	},
	"2001 KD77|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.123, "V-R": 0.624, "R-I": 0.565}, "sun": True
	},
	"2001 KG77|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.440}, "sun": True
	},
	"2001 QC298|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.490, "R-I": 0.480}, "sun": True
	},
	"2001 QR322|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.800, "V-R": 0.460, "R-I": 0.360}, "sun": True
	},
	"2001 QX322|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.914, "V-R": 0.562}, "sun": True
	},
	"2001 XZ255|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.224, "V-R": 0.709}, "sun": True
	},
	"2002 GH32|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.990, "V-R": 0.570, "R-I": 0.590}, "sun": True
	},
	"2002 PQ152|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.130, "V-R": 0.720}, "sun": True
	},
	"2002 XV93|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.375}, "sun": True
	},
	"2003 FZ129|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.840, "V-R": 0.480, "R-I": 0.460}, "sun": True
	},
	"2003 QA92|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.040, "V-R": 0.630}, "sun": True
	},
	"2003 QK91|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.870, "V-R": 0.500, "R-I": 0.470}, "sun": True
	},
	"2003 QQ91|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.670, "V-R": 0.510}, "sun": True
	},
	"2003 UY291|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.880, "V-R": 0.510, "R-I": 0.670}, "sun": True
	},
	"2003 WN188|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.780, "V-R": 0.480, "R-I": 0.500}, "sun": True
	},
	"2004 DA62|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.520, "R-I": 0.550}, "sun": True
	},
	"2004 OJ14|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.900, "V-R": 0.520, "R-I": 0.540}, "sun": True
	},
	"2004 XR190|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.450, "R-I": 0.520}, "sun": True
	},
	"2005 TN53|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.470, "R-I": 0.470}, "sun": True
	},
	"2006 RJ103|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.470, "R-I": 0.270}, "sun": True
	},
	"2007 VH305|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.690, "V-R": 0.491, "R-I": 0.480}, "sun": True
	},
	"2009 YG19|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.000, "V-R": 0.610}, "sun": True
	},
	"2010 BK118|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.794, "V-R": 0.525, "R-I": 0.480}, "sun": True
	},
	"2010 BL4|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.860, "V-R": 0.390, "R-I": 0.470}, "sun": True
	},
	"2010 OM101|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.795, "V-R": 0.588, "R-I": 0.360}, "sun": True
	},
	"2010 OR1|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.781, "V-R": 0.517, "R-I": 0.447}, "sun": True
	},
	"2010 TS191|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.760, "V-R": 0.390}, "sun": True
	},
	"2010 TT191|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.470}, "sun": True
	},
	"2010 WG9|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.781, "V-R": 0.492, "R-I": 0.458}, "sun": True
	},
	"2011 HM102|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.410, "R-I": 0.520}, "sun": True
	},
	"2012 DR30|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.647, "V-R": 0.563, "R-I": 0.422}, "sun": True
	},
	"2012 VP113|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.520, "R-I": 0.530}, "sun": True
	},
	"2013 AZ60|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.540}, "sun": True
	},
	"2013 BL76|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.450}, "sun": True
	},
	"2013 BO16|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 1.140, "V-R": 0.650}, "sun": True
	},
	"2013 CX217|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.280}, "sun": True
	},
	"2013 CY197|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.880, "V-R": 0.510, "R-I": 0.610}, "sun": True
	},
	"2013 KY18|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.760, "V-R": 0.360}, "sun": True
	},
	"2013 LD16|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.860, "V-R": 0.440}, "sun": True
	},
	"2013 NS11|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.560}, "sun": True
	},
	"2013 TZ158|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.536, "R-I": 0.497}, "sun": True
	},
	"2013 YG48|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.800, "V-R": 0.515}, "sun": True
	},
	"2014 CW14|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.870, "V-R": 0.510}, "sun": True
	},
	"2014 QO441|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.470}, "sun": True
	},
    "(433) Eros|11": {
        "nm": list(range(350, 895, 5)),
        "br": [0.39114, 0.40755, 0.43474, 0.48806, 0.49886, 0.51646, 0.49042, 0.44175, 0.53512, 0.55996, 0.62863, 0.6198, 0.67636, 0.66499, 0.68589, 0.67764,
        0.68227, 0.73805, 0.7302, 0.76963, 0.7911, 0.8021, 0.8124, 0.81771, 0.82751, 0.8589, 0.87197, 0.89604, 0.89299, 0.90126, 0.91716, 0.91591, 0.91854,
        0.92926, 0.93106, 0.95902, 0.96679, 0.97107, 0.96876, 0.98038, 1.0, 0.9954, 0.98526, 1.00648, 0.98666, 1.01316, 1.01612, 1.02944, 1.02794, 1.05006,
        1.0472, 1.05417, 1.06109, 1.05626, 1.06517, 1.0627, 1.0777, 1.08487, 1.08937, 1.08957, 1.10265, 1.1198, 1.11823, 1.12239, 1.12993, 1.1458, 1.13856,
        1.12816, 1.13752, 1.14195, 1.12574, 1.14946, 1.13265, 1.17224, 1.12637, 1.13412, 1.15489, 1.16516, 1.13524, 1.13512, 1.16729, 1.19448, 1.21084,
        1.15377, 1.12806, 1.17343, 1.21881, 1.14669, 1.14314, 1.14373, 1.16095, 1.09179, 1.0755, 1.13114, 1.16251, 1.21117, 1.13878, 1.20665, 1.0951, 1.047,
        1.00354, 0.9945, 1.01803, 1.14228, 1.05281, 1.18387, 1.09958, 1.16424, 0.91067],
        "albedo": 0.098 # https://www.lpi.usra.edu/meetings/lpsc2004/pdf/2080.pdf
    },
	"(1172) Aneas|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.727, "V-R": 0.510, "R-I": 0.400}, "sun": True
	},
	"(1173) Anchises|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.811, "V-R": 0.402, "R-I": 0.403}, "sun": True
	},
	"(1871) Astyanax|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.716, "V-R": 0.456, "R-I": 0.424}, "sun": True
	},
	"(2060) Chiron|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.660, "V-R": 0.359, "R-I": 0.324}, "sun": True
	},
	"(2223) Sarpedon|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.753, "V-R": 0.465, "R-I": 0.440}, "sun": True
	},
	"(2357) Phereclos|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.718, "V-R": 0.427, "R-I": 0.463}, "sun": True
	},
	"(3548) Eurybates|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.677, "V-R": 0.352, "R-I": 0.339}, "sun": True
	},
	"(4035) 1986 WD|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.752, "V-R": 0.484, "R-I": 0.451}, "sun": True
	},
	"(4829) Sergestus|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.851, "V-R": 0.420, "R-I": 0.372}, "sun": True
	},
	"(5130) Ilioneus|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.763, "V-R": 0.481, "R-I": 0.424}, "sun": True
	},
	"(5145) Pholus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.261, "V-R": 0.791, "R-I": 0.818}, "sun": True
	},
	"(5511) Cloanthus|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.906, "V-R": 0.442, "R-I": 0.526}, "sun": True
	},
	"(6545) 1986 TR6|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.734, "V-R": 0.499, "R-I": 0.436}, "sun": True
	},
	"(6998) Tithonus|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.787, "V-R": 0.455, "R-I": 0.438}, "sun": True
	},
	"(7066) Nessus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.090, "V-R": 0.763, "R-I": 0.689}, "sun": True
	},
	"(7352) 1994 CO|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.713, "V-R": 0.417, "R-I": 0.397}, "sun": True
	},
	"(8405) Asbolus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.738, "V-R": 0.508, "R-I": 0.505}, "sun": True
	},
	"(9030) 1989 UX5|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.887, "V-R": 0.493, "R-I": 0.480}, "sun": True
	},
	"(9430) Erichthonio|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.742, "V-R": 0.488, "R-I": 0.456}, "sun": True
	},
	"(9818) Eurymachos|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.673, "V-R": 0.339, "R-I": 0.355}, "sun": True
	},
	"(10199) Chariklo|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.802, "V-R": 0.491, "R-I": 0.519}, "sun": True
	},
	"(10370) Hylonome|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.690, "V-R": 0.469, "R-I": 0.496}, "sun": True
	},
	"(11089) 1994 CS8|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.689, "V-R": 0.423, "R-I": 0.384}, "sun": True
	},
	"(11351) Leucus|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.739, "V-R": 0.498, "R-I": 0.402}, "sun": True
	},
	"(11488) 1988 RM11|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.777, "V-R": 0.436, "R-I": 0.420}, "sun": True
	},
	"(11663) 1997 GO24|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.837, "V-R": 0.409, "R-I": 0.463}, "sun": True
	},
	"(12917) 1998 TG16|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.724, "V-R": 0.537, "R-I": 0.410}, "sun": True
	},
	"(12921) 1998 WZ5|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.673, "V-R": 0.403, "R-I": 0.380}, "sun": True
	},
	"(13463) Antiphos|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.692, "V-R": 0.449, "R-I": 0.412}, "sun": True
	},
	"(14707) 2000 CC20|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.752, "V-R": 0.412, "R-I": 0.385}, "sun": True
	},
	"(15094) Polymele|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.652, "V-R": 0.477, "R-I": 0.322}, "sun": True
	},
	"(15502) 1999 NV27|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.766, "V-R": 0.445, "R-I": 0.430}, "sun": True
	},
	"(15504) 1999 RG33|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.817, "V-R": 0.495, "R-I": 0.350}, "sun": True
	},
	"(15535) 2000 AT177|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.739, "V-R": 0.470, "R-I": 0.461}, "sun": True
	},
	"(15760) Albion|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.869, "V-R": 0.707, "R-I": 0.651}, "sun": True
	},
	"(15788) 1993 SB|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.802, "V-R": 0.475, "R-I": 0.514}, "sun": True
	},
	"(15789) 1993 SC|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.045, "V-R": 0.688, "R-I": 0.697}, "sun": True
	},
	"(15810) Arawn|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.010, "V-R": 0.632, "R-I": 0.538}, "sun": True
	},
	"(15820) 1994 TB|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.107, "V-R": 0.697, "R-I": 0.739}, "sun": True
	},
	"(15874) 1996 TL66|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.687, "V-R": 0.369, "R-I": 0.370}, "sun": True
	},
	"(15875) 1996 TP66|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.031, "V-R": 0.655, "R-I": 0.673}, "sun": True
	},
	"(15883) 1997 CR29|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.538, "R-I": 0.620}, "sun": True
	},
	"(15977) 1998 MA11|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.748, "V-R": 0.465, "R-I": 0.441}, "sun": True
	},
	"(16684) 1994 JQ1|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.134, "V-R": 0.736, "R-I": 0.650}, "sun": True
	},
	"(17416) 1988 RR10|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.742, "V-R": 0.488, "R-I": 0.498}, "sun": True
	},
	"(18060) 1999 XJ156|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.758, "V-R": 0.412, "R-I": 0.364}, "sun": True
	},
	"(18137) 2000 OU30|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.733, "V-R": 0.496, "R-I": 0.409}, "sun": True
	},
	"(18268) Dardanos|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.795, "V-R": 0.529, "R-I": 0.451}, "sun": True
	},
	"(18493) Demoleon|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.703, "V-R": 0.395, "R-I": 0.380}, "sun": True
	},
	"(18940) 2000 QV49|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.709, "V-R": 0.465, "R-I": 0.429}, "sun": True
	},
	"(19255) 1994 VK8|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.010, "V-R": 0.659, "R-I": 0.490}, "sun": True
	},
	"(19299) 1996 SZ4|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.754, "V-R": 0.522, "R-I": 0.446}, "sun": True
	},
	"(19308) 1996 TO66|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.671, "V-R": 0.389, "R-I": 0.356}, "sun": True
	},
	"(19521) Chaos|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.932, "V-R": 0.608, "R-I": 0.571}, "sun": True
	},
	"(20000) Varuna|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.906, "V-R": 0.626, "R-I": 0.628}, "sun": True
	},
	"(20108) 1995 QZ9|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.880, "V-R": 0.515}, "sun": True
	},
	"(20738) 1999 XG191|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.776, "V-R": 0.472, "R-I": 0.467}, "sun": True
	},
	"(23549) Epicles|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.800, "V-R": 0.485, "R-I": 0.387}, "sun": True
	},
	"(23694) 1997 KZ3|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.723, "V-R": 0.474, "R-I": 0.418}, "sun": True
	},
	"(24233) 1999 XD94|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.704, "V-R": 0.481, "R-I": 0.418}, "sun": True
	},
	"(24341) 2000 AJ87|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.713, "V-R": 0.369, "R-I": 0.390}, "sun": True
	},
	"(24380) 2000 AA160|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.734, "V-R": 0.391, "R-I": 0.336}, "sun": True
	},
	"(24390) 2000 AD177|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.700, "V-R": 0.513, "R-I": 0.462}, "sun": True
	},
	"(24420) 2000 BU22|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.937, "V-R": 0.441, "R-I": 0.304}, "sun": True
	},
	"(24426) 2000 CR12|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.717, "V-R": 0.414, "R-I": 0.424}, "sun": True
	},
	"(24444) 2000 OP32|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.712, "V-R": 0.437, "R-I": 0.409}, "sun": True
	},
	"(24452) 2000 QU167|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.872, "V-R": 0.441, "R-I": 0.406}, "sun": True
	},
	"(24467) 2000 SS165|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.927, "V-R": 0.460, "R-I": 0.513}, "sun": True
	},
	"(24835) 1995 SM55|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.652, "V-R": 0.357, "R-I": 0.356}, "sun": True
	},
	"(24952) 1997 QJ4|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.763, "V-R": 0.431, "R-I": 0.396}, "sun": True
	},
	"(24978) 1998 HJ151|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.110, "V-R": 0.710}, "sun": True
	},
    "(25143) Itokawa|12": {
        "nm": list(range(325, 1025, 25)),
        "br": [0.388, 0.568, 0.676, 0.773, 0.824, 0.856, 0.888, 0.914, 0.964, 1.0, 1.036, 1.058, 1.076, 1.094, 1.122, 1.140, 1.147, 1.144, 1.129, 1.101,
        1.068, 1.029, 1.0, 0.978, 0.975, 0.946, 0.917, 0.935],
        "albedo": 0.29 # https://academic.oup.com/pasj/article/66/3/52/1438030
    },
	"(25347) 1999 RQ116|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.618, "V-R": 0.488, "R-I": 0.461}, "sun": True
	},
	"(26181) 1996 GQ21|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.999, "V-R": 0.697, "R-I": 0.694}, "sun": True
	},
	"(26308) 1998 SM165|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.989, "V-R": 0.641, "R-I": 0.666}, "sun": True
	},
	"(26375) 1999 DE9|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.967, "V-R": 0.579, "R-I": 0.568}, "sun": True
	},
	"(28958) 2001 CQ42|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.730, "V-R": 0.364, "R-I": 0.230}, "sun": True
	},
	"(28978) Ixion|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.018, "V-R": 0.605, "R-I": 0.580}, "sun": True
	},
	"(29981) 1999 TD10|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.808, "V-R": 0.502, "R-I": 0.511}, "sun": True
	},
	"(30698) Hippokoon|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.715, "V-R": 0.458, "R-I": 0.412}, "sun": True
	},
	"(31820) 1999 RT186|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.889, "V-R": 0.520, "R-I": 0.396}, "sun": True
	},
	"(31821) 1999 RK225|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.980, "V-R": 0.440, "R-I": 0.461}, "sun": True
	},
	"(31824) Elatus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.020, "V-R": 0.620, "R-I": 0.630}, "sun": True
	},
	"(32430) 2000 RQ83|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.772, "V-R": 0.474, "R-I": 0.425}, "sun": True
	},
	"(32532) Thereus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.764, "V-R": 0.501, "R-I": 0.479}, "sun": True
	},
	"(32615) 2001 QU277|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.807, "V-R": 0.452, "R-I": 0.474}, "sun": True
	},
	"(32794) 1989 UE5|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.923, "V-R": 0.393, "R-I": 0.486}, "sun": True
	},
	"(32929) 1995 QY9|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.561}, "sun": True
	},
	"(33001) 1997 CU29|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.157, "V-R": 0.645, "R-I": 0.634}, "sun": True
	},
	"(33128) 1998 BU48|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.044, "V-R": 0.631, "R-I": 0.644}, "sun": True
	},
	"(33340) 1998 VG44|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.955, "V-R": 0.555, "R-I": 0.598}, "sun": True
	},
	"(34785) 2001 RG87|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.728, "V-R": 0.386, "R-I": 0.419}, "sun": True
	},
	"(35671) 1998 SN165|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.712, "V-R": 0.444, "R-I": 0.437}, "sun": True
	},
	"(38083) Rhadamanth|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.650, "V-R": 0.527, "R-I": 0.412}, "sun": True
	},
	"(38084) 1999 HB12|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.893, "V-R": 0.544, "R-I": 0.481}, "sun": True
	},
	"(38628) Huya|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.963, "V-R": 0.609, "R-I": 0.593}, "sun": True
	},
	"(39285) 2001 BP75|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.381, "R-I": 0.291}, "sun": True
	},
	"(40314) 1999 KR16|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.123, "V-R": 0.738, "R-I": 0.750}, "sun": True
	},
	"(42301) 2001 UR163|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 1.290, "V-R": 0.839, "R-I": 0.673}, "sun": True
	},
	"(42355) Typhon|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.758, "V-R": 0.518, "R-I": 0.378}, "sun": True
	},
	"(44594) 1999 OX3|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.138, "V-R": 0.708, "R-I": 0.640}, "sun": True
	},
	"(47171) Lempo|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.029, "V-R": 0.693, "R-I": 0.619}, "sun": True
	},
	"(47932) 2000 GN171|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.960, "V-R": 0.607, "R-I": 0.617}, "sun": True
	},
	"(47967) 2000 SL298|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.899, "V-R": 0.489, "R-I": 0.476}, "sun": True
	},
	"(48249) 2001 SY345|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.758, "V-R": 0.530, "R-I": 0.420}, "sun": True
	},
	"(48252) 2001 TL212|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.949, "V-R": 0.467, "R-I": 0.436}, "sun": True
	},
	"(48639) 1995 TL8|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.008, "V-R": 0.621, "R-I": 0.551}, "sun": True
	},
	"(49036) Pelion|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.746, "V-R": 0.556, "R-I": 0.368}, "sun": True
	},
	"(50000) Quaoar|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.958, "V-R": 0.650, "R-I": 0.610}, "sun": True
	},
	"(51359) 2000 SC17|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.864, "V-R": 0.447, "R-I": 0.438}, "sun": True
	},
	"(52747) 1998 HM151|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.930, "V-R": 0.620}, "sun": True
	},
	"(52872) Okyrhoe|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.743, "V-R": 0.495, "R-I": 0.480}, "sun": True
	},
	"(52975) Cyllarus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.096, "V-R": 0.680, "R-I": 0.669}, "sun": True
	},
	"(53469) 2000 AX8|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.663, "V-R": 0.356, "R-I": 0.361}, "sun": True
	},
	"(54598) Bienor|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.711, "V-R": 0.476, "R-I": 0.400}, "sun": True
	},
	"(55565) 2002 AW197|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.915, "V-R": 0.589, "R-I": 0.581}, "sun": True
	},
	"(55576) Amycus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.111, "V-R": 0.705, "R-I": 0.666}, "sun": True
	},
	"(55636) 2002 TX300|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.679, "V-R": 0.359, "R-I": 0.323}, "sun": True
	},
	"(55637) 2002 UX25|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.979, "V-R": 0.552}, "sun": True
	},
	"(55638) 2002 VE95|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.094, "V-R": 0.733, "R-I": 0.760}, "sun": True
	},
	"(56968) 2000 SA92|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.986, "V-R": 0.494, "R-I": 0.509}, "sun": True
	},
	"(58534) Logos|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.990, "V-R": 0.729, "R-I": 0.602}, "sun": True
	},
	"(59358) 1999 CL158|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.800, "V-R": 0.390, "R-I": 0.470}, "sun": True
	},
	"(60454) 2000 CH105|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.019, "V-R": 0.643, "R-I": 0.583}, "sun": True
	},
	"(60458) 2000 CM114|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.730, "V-R": 0.500}, "sun": True
	},
	"(60558) Echeclus|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.841, "V-R": 0.502, "R-I": 0.486}, "sun": True
	},
	"(60608) 2000 EE173|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.665, "V-R": 0.488, "R-I": 0.543}, "sun": True
	},
	"(60620) 2000 FD8|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 1.151, "V-R": 0.664, "R-I": 0.648}, "sun": True
	},
	"(60621) 2000 FE8|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.750, "V-R": 0.480, "R-I": 0.500}, "sun": True
	},
	"(63252) 2001 BL41|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.718, "V-R": 0.509, "R-I": 0.381}, "sun": True
	},
	"(65150) 2002 CA126|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.651, "V-R": 0.377, "R-I": 0.407}, "sun": True
	},
	"(65225) 2002 EK44|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.693, "V-R": 0.401, "R-I": 0.334}, "sun": True
	},
	"(65407) 2002 RP120|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.846, "V-R": 0.489, "R-I": 0.484}, "sun": True
	},
	"(65489) Ceto|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.879, "V-R": 0.547, "R-I": 0.411}, "sun": True
	},
	"(66452) 1999 OF4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.032, "V-R": 0.673, "R-I": 0.601}, "sun": True
	},
	"(66652) Borasisi|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.646, "R-I": 0.647}, "sun": True
	},
	"(69986) 1998 WW24|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.756, "V-R": 0.463, "R-I": 0.659}, "sun": True
	},
	"(69988) 1998 WA31|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.786, "V-R": 0.492, "R-I": 0.530}, "sun": True
	},
	"(69990) 1998 WU31|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.505, "R-I": 0.722}, "sun": True
	},
	"(73480) 2002 PN34|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.818, "V-R": 0.514}, "sun": True
	},
	"(76804) 2000 QE|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.803, "V-R": 0.446, "R-I": 0.443}, "sun": True
	},
	"(79360) Sila-Nunam|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.055, "V-R": 0.666, "R-I": 0.609}, "sun": True
	},
	"(79978) 1999 CC158|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.996, "V-R": 0.611, "R-I": 0.619}, "sun": True
	},
	"(79983) 1999 DF9|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.710, "R-I": 0.650}, "sun": True
	},
	"(82075) 2000 YW134|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.922, "V-R": 0.503, "R-I": 0.581}, "sun": True
	},
	"(82155) 2001 FZ173|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.864, "V-R": 0.546, "R-I": 0.508}, "sun": True
	},
	"(82158) 2001 FP185|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.572, "R-I": 0.458}, "sun": True
	},
	"(83982) Crantor|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.105, "V-R": 0.761, "R-I": 0.667}, "sun": True
	},
	"(84522) 2002 TC302|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 1.067, "V-R": 0.655, "R-I": 0.660}, "sun": True
	},
	"(84709) 2002 VW120|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.855, "V-R": 0.462, "R-I": 0.548}, "sun": True
	},
	"(84719) 2002 VR128|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.935, "V-R": 0.605}, "sun": True
	},
	"(84922) 2003 VS2|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.930, "V-R": 0.590}, "sun": True
	},
	"(85633) 1998 KR65|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.095, "V-R": 0.628, "R-I": 0.790}, "sun": True
	},
	"(86047) 1999 OY3|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.726, "V-R": 0.345, "R-I": 0.277}, "sun": True
	},
	"(86177) 1999 RY215|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.719, "V-R": 0.358, "R-I": 0.631}, "sun": True
	},
	"(87269) 2000 OO67|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.080, "V-R": 0.654, "R-I": 0.593}, "sun": True
	},
	"(87555) 2000 QB243|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.763, "V-R": 0.383, "R-I": 0.729}, "sun": True
	},
	"(88269) 2001 KF77|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.080, "V-R": 0.730}, "sun": True
	},
	"(90377) Sedna|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 1.179, "V-R": 0.739, "R-I": 0.654}, "sun": True
	},
	"(90482) Orcus|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.670, "V-R": 0.376, "R-I": 0.372}, "sun": True
	},
	"(90568) 2004 GV9|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.895, "V-R": 0.520}, "sun": True
	},
	"(91133) 1998 HK151|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.645, "V-R": 0.520, "R-I": 0.390}, "sun": True
	},
	"(91205) 1998 US43|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.691, "V-R": 0.446, "R-I": 0.347}, "sun": True
	},
	"(91554) 1999 RZ215|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.771, "V-R": 0.575, "R-I": 0.539}, "sun": True
	},
	"(95626) 2002 GZ32|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.674, "V-R": 0.576, "R-I": 0.538}, "sun": True
	},
	"(99328) 2001 UY123|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.890, "V-R": 0.537, "R-I": 0.434}, "sun": True
	},
	"(105685) 2000 SC51|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 1.016, "V-R": 0.444, "R-I": 0.452}, "sun": True
	},
	"(111113) 2001 VK85|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.822, "V-R": 0.462, "R-I": 0.558}, "sun": True
	},
	"(118228) 1996 TQ66|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.186, "V-R": 0.670, "R-I": 0.746}, "sun": True
	},
	"(118379) 1999 HC12|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.894, "V-R": 0.490, "R-I": 0.343}, "sun": True
	},
	"(118702) 2000 OM67|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.470, "R-I": 0.590}, "sun": True
	},
	"(119068) 2001 KC77|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.910, "V-R": 0.560}, "sun": True
	},
	"(119315) 2001 SQ73|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.670, "V-R": 0.460}, "sun": True
	},
	"(119951) 2002 KX14|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.050, "V-R": 0.607}, "sun": True
	},
	"(119979) 2002 WC19|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 1.040, "V-R": 0.630}, "sun": True
	},
	"(120061) 2003 CO1|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.743, "V-R": 0.472, "R-I": 0.494}, "sun": True
	},
	"(120132) 2003 FY128|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 1.021, "V-R": 0.614, "R-I": 0.540}, "sun": True
	},
	"(120178) 2003 OP32|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.662, "V-R": 0.375, "R-I": 0.305}, "sun": True
	},
	"(120181) 2003 UR292|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.025, "V-R": 0.635}, "sun": True
	},
	"(120216) 2004 EW95|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.693, "V-R": 0.375, "R-I": 0.215}, "sun": True
	},
	"(120347) Salacia|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.664, "V-R": 0.403, "R-I": 0.433}, "sun": True
	},
	"(120348) 2004 TY364|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.059, "V-R": 0.601, "R-I": 0.520}, "sun": True
	},
	"(120453) 1988 RE12|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.826, "V-R": 0.388, "R-I": 0.483}, "sun": True
	},
	"(121725) Aphidas|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.060, "V-R": 0.648, "R-I": 0.679}, "sun": True
	},
	"(124729) 2001 SB173|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.992, "V-R": 0.503, "R-I": 0.424}, "sun": True
	},
	"(127546) 2002 XU93|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.731, "V-R": 0.410, "R-I": 0.443}, "sun": True
	},
	"(129772) 1999 HR11|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.530, "R-I": 0.800}, "sun": True
	},
    "(134340) Pluto|6": {
        "nm": [400.551, 423.678, 440.749, 458.37, 466.079, 493.062, 496.366, 499.119, 553.634, 555.837, 559.692, 582.819, 587.225, 630.727, 658.811, 
        670.925, 680.286, 697.907, 729.846, 761.233, 762.885, 773.348, 784.912, 790.419, 795.925, 803.084, 807.489, 812.996, 816.85, 836.674],
        "br": [0.642, 0.695, 0.766, 0.799, 0.832, 0.887, 0.872, 0.902, 1.019, 1.012, 1.031, 1.056, 1.07, 1.121, 1.137, 0.735, 1.156, 1.169, 1.152, 
        1.18, 1.157, 1.172, 1.099, 1.144, 1.118, 0.988, 1.072, 1.062, 1.135, 1.169],
		"albedo": 0.52
    },
	"(134340) Pluto|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.867, "V-R": 0.515, "R-I": 0.400}, "albedo": 0.52, "sun": True
	},
	"(134860) 2000 OJ67|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.050, "V-R": 0.670, "R-I": 0.600}, "sun": True
	},
	"(135182) 2001 QT322|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.710, "V-R": 0.530}, "sun": True
	},
	"(136108) Haumea|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.633, "V-R": 0.353, "R-I": 0.330}, "sun": True
	},
    "(136199) Eris|6": {
        "nm": [417.357, 479.507, 532.699, 585.89, 601.008, 604.367, 622.844, 637.962, 653.08, 656.439, 659.239, 673.236, 679.955, 692.273, 702.912, 
        712.43, 734.267, 740.426, 747.704, 750.504, 765.062, 779.059, 788.578, 793.617, 809.295, 813.774, 826.652, 841.209, 860.246],
        "br": [0.995, 1.059, 1.084, 1.101, 1.08, 1.104, 1.111, 1.103, 1.121, 1.104, 1.11, 1.097, 1.117, 1.034, 1.121, 1.13, 1.11, 1.073, 1.11, 1.077, 
        1.132, 1.138, 1.087, 1.126, 1.018, 1.079, 0.881, 1.072, 1.13]
    },
	"(136199) Eris|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.781, "V-R": 0.393, "R-I": 0.363}, "sun": True
	},
	"(136204) 2003 WL7|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.480}, "sun": True
	},
    "(136472) Makemake|6": {
        "nm": [417.357, 466.069, 588.13, 601.568, 609.406, 631.243, 642.441, 649.72, 656.439, 664.278, 672.116, 679.955, 691.153, 706.271, 715.789,
        723.628, 729.787, 740.426, 744.345, 751.064, 766.181, 782.419, 788.578, 794.737, 809.295, 813.774, 826.652, 841.209, 860.246],
        "br": [0.89, 0.971, 1.106, 1.059, 1.127, 1.133, 1.125, 1.157, 1.137, 1.155, 1.116, 1.139, 1.03, 1.179, 1.182, 1.143, 1.163, 1.088, 1.16, 1.084,
        1.201, 1.201, 1.087, 1.159, 1.018, 1.079, 0.881, 1.072, 1.13]
    },
	"(136472) Makemake|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.840, "V-R": 0.480}, "sun": True
	},
	"(137294) 1999 RE215|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.003, "V-R": 0.710, "R-I": 0.571}, "sun": True
	},
	"(137295) 1999 RB216|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.897, "V-R": 0.522, "R-I": 0.506}, "sun": True
	},
	"(138537) 2000 OK67|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.821, "V-R": 0.583, "R-I": 0.524}, "sun": True
	},
	"(143707) 2003 UY117|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.950, "V-R": 0.590}, "sun": True
	},
	"(144897) 2004 UX10|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.950, "V-R": 0.575}, "sun": True
	},
	"(145451) 2005 RM43|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.590, "V-R": 0.390}, "sun": True
	},
	"(145452) 2005 RN43|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.940, "V-R": 0.592, "R-I": 0.486}, "sun": True
	},
	"(145453) 2005 RR43|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.389}, "sun": True
	},
	"(145480) 2005 TB190|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.980, "V-R": 0.562, "R-I": 0.578}, "sun": True
	},
	"(145486) 2005 UJ438|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.946, "V-R": 0.641, "R-I": 0.510}, "sun": True
	},
	"(148209) 2000 CR105|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.771, "V-R": 0.509, "R-I": 0.590}, "sun": True
	},
	"(148975) 2001 XA255|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.680, "R-I": 0.440}, "sun": True
	},
	"(160427) 2005 RL43|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.120, "V-R": 0.730}, "sun": True
	},
	"(163135) 2002 CT22|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.690, "V-R": 0.382, "R-I": 0.360}, "sun": True
	},
	"(168703) 2000 GP183|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.669, "V-R": 0.445, "R-I": 0.463}, "sun": True
	},
	"(174567) Varda|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.892, "V-R": 0.556, "R-I": 0.510}, "sun": True
	},
	"(181708) 1993 FW|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.023, "V-R": 0.583, "R-I": 0.439}, "sun": True
	},
	"(181855) 1998 WT31|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.774, "V-R": 0.453, "R-I": 0.326}, "sun": True
	},
	"(181874) 1999 HW11|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.840, "V-R": 0.499, "R-I": 0.493}, "sun": True
	},
	"(182397) 2001 QW297|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.020, "V-R": 0.580, "R-I": 0.670}, "sun": True
	},
	"(182934) 2002 GJ32|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.330, "V-R": 0.590, "R-I": 0.420}, "sun": True
	},
	"(192388) 1996 RD29|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.741, "V-R": 0.421, "R-I": 0.388}, "sun": True
	},
	"(192929) 2000 AT44|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.707, "V-R": 0.354, "R-I": 0.318}, "sun": True
	},
	"(208996) 2003 AZ84|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.738, "V-R": 0.430, "R-I": 0.473}, "sun": True
	},
	"(248835) 2006 SX368|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.758, "V-R": 0.478, "R-I": 0.471}, "sun": True
	},
	"(250112) 2002 KY14|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.060, "V-R": 0.709, "R-I": 0.650}, "sun": True
	},
	"(275809) 2001 QY297|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.947, "V-R": 0.479, "R-I": 0.651}, "sun": True
	},
	"(278361) 2007 JJ43|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.020, "V-R": 0.590, "R-I": 0.500}, "sun": True
	},
	"(281371) 2008 FC76|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.987, "V-R": 0.685, "R-I": 0.652}, "sun": True
	},
	"(303775) 2005 QU182|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.877, "V-R": 0.593}, "sun": True
	},
	"(307261) 2002 MS4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.690, "V-R": 0.380}, "sun": True
	},
	"(307982) 2004 PG115|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.966, "V-R": 0.664, "R-I": 0.633}, "sun": True
	},
	"(308933) 2006 SQ372|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.030, "V-R": 0.590, "R-I": 0.650}, "sun": True
	},
	"(309139) 2006 XQ51|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.410}, "sun": True
	},
	"(309737) 2008 SJ236|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.010, "V-R": 0.588, "R-I": 0.500}, "sun": True
	},
	"(309741) 2008 UZ6|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.590}, "sun": True
	},
	"(315898) 2008 QD4|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.460}, "sun": True
	},
	"(316431) 2010 TH167|9": {"tags": ["solar_system", "minor_body", "asteroid", "trojan", "trojan-j"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.460}, "sun": True
	},
	"(330759) 2008 SO218|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.890, "V-R": 0.550, "R-I": 0.500}, "sun": True
	},
	"(336756) 2010 NV1|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.765, "V-R": 0.512, "R-I": 0.390}, "sun": True
	},
	"(341275) 2007 RG283|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.790, "V-R": 0.470}, "sun": True
	},
	"(341520) Mors-Somn|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 1.290, "V-R": 0.740, "R-I": 0.630}, "sun": True
	},
	"(342842) 2008 YB3|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.774, "V-R": 0.472, "R-I": 0.490}, "sun": True
	},
	"(346889) Rhiphonos|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.550}, "sun": True
	},
	"(349933) 2009 YF7|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.460}, "sun": True
	},
	"(382004) 2010 RM64|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.000, "V-R": 0.550}, "sun": True
	},
	"(385185) 1993 RO|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.590, "R-I": 0.480}, "sun": True
	},
	"(385191) 1997 RT5|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.075, "V-R": 0.474, "R-I": 0.539}, "sun": True
	},
	"(385194) 1998 KG62|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.039, "V-R": 0.609, "R-I": 0.610}, "sun": True
	},
	"(385199) 1999 OE4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.103, "V-R": 0.567, "R-I": 0.414}, "sun": True
	},
	"(385437) 2003 GH55|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.120, "V-R": 0.665, "R-I": 0.859}, "sun": True
	},
	"(385571) Otrera|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.420, "R-I": 0.460}, "sun": True
	},
	"(385607) 2005 EO297|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.840, "V-R": 0.480, "R-I": 0.570}, "sun": True
	},
	"(385695) 2005 TO74|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.850, "V-R": 0.490, "R-I": 0.420}, "sun": True
	},
	"(416400) 2003 UZ117|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.663, "V-R": 0.354, "R-I": 0.335}, "sun": True
	},
	"(418993) 2009 MS9|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.840, "V-R": 0.520}, "sun": True
	},
	"(427507) 2002 DH5|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.663, "V-R": 0.391, "R-I": 0.416}, "sun": True
	},
	"(444030) 2004 NT33|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.641, "V-R": 0.403, "R-I": 0.403}, "sun": True
	},
	"(445473) 2010 VZ98|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 1.100, "V-R": 0.670}, "sun": True
	},
	"(447178) 2005 RO43|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.770, "V-R": 0.470}, "sun": True
	},
	"(449097) 2012 UT68|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.020, "V-R": 0.660}, "sun": True
	},
	"(455171) 1999 OM4|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.137, "V-R": 0.602, "R-I": 0.499}, "sun": True
	},
	"(459865) 2013 XZ8|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.450}, "sun": True
	},
	"(459971) 2014 ON6|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.970, "V-R": 0.580}, "sun": True
	},
	"(463368) 2012 VU85|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.070, "V-R": 0.630}, "sun": True
	},
	"(463663) 2014 HY123|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.670, "V-R": 0.490}, "sun": True
	},
	"(469306) 1999 CD158|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.864, "V-R": 0.520, "R-I": 0.575}, "sun": True
	},
	"(469333) 2000 PE30|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.752, "V-R": 0.373, "R-I": 0.410}, "sun": True
	},
	"(469362) 2001 KB77|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.890, "V-R": 0.457, "R-I": 0.548}, "sun": True
	},
	"(469372) 2001 QF298|9": {"tags": ["solar_system", "minor_body", "tno", "plutino"],
		"filters": "Landolt", "indices": {"B-V": 0.695, "V-R": 0.388, "R-I": 0.360}, "sun": True
	},
	"(469750) 2005 PU21|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 1.140, "V-R": 0.650, "R-I": 0.680}, "sun": True
	},
	"(470316) 2007 OC10|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.876, "V-R": 0.553, "R-I": 0.471}, "sun": True
	},
	"(470599) 2008 OG19|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.940, "V-R": 0.530, "R-I": 0.590}, "sun": True
	},
	"(471339) 2011 ON45|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.110, "V-R": 0.705}, "sun": True
	},
	"(474640) 2004 VN112|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.900, "V-R": 0.520, "R-I": 0.450}, "sun": True
	},
	"(506479) 2003 HB57|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.830, "V-R": 0.480, "R-I": 0.540}, "sun": True
	},
	"(508770) 1995 WY2|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.030, "V-R": 0.600, "R-I": 0.510}, "sun": True
	},
	"(523588) 2000 CN105|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.100, "V-R": 0.636, "R-I": 0.640}, "sun": True
	},
	"(523591) 2001 QD298|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.970, "V-R": 0.670}, "sun": True
	},
	"(523597) 2002 QX47|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.700, "V-R": 0.380}, "sun": True
	},
	"(523620) 2007 RH283|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.430}, "sun": True
	},
	"(523622) 2007 TG422|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.880, "V-R": 0.510, "R-I": 0.510}, "sun": True
	},
	"(523676) 2013 UL10|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.970, "V-R": 0.670}, "sun": True
	},
	"(523785) 2015 CM3|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 1.210, "V-R": 0.570}, "sun": True
	},
	"(523899) 1997 CV29|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 1.210, "V-R": 0.650}, "sun": True
	},
	"(523965) 1998 XY95|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.930, "V-R": 0.720, "R-I": 0.752}, "sun": True
	},
	"(523983) 1999 RY214|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-h"],
		"filters": "Landolt", "indices": {"B-V": 0.693, "V-R": 0.565, "R-I": 0.530}, "sun": True
	},
	"(524049) 2000 CQ105|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.671, "V-R": 0.449, "R-I": 0.346}, "sun": True
	},
	"(524217) 2001 RZ143|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 1.080, "V-R": 0.510, "R-I": 0.490}, "sun": True
	},
	"(524834) 2003 YL179|9": {"tags": ["solar_system", "minor_body", "tno", "classical", "classical-c"],
		"filters": "Landolt", "indices": {"B-V": 0.810, "V-R": 0.450}, "sun": True
	},
	"(525815) 2005 SD278|9": {"tags": ["solar_system", "minor_body", "tno", "resonant"],
		"filters": "Landolt", "indices": {"B-V": 0.970, "V-R": 0.560, "R-I": 0.530}, "sun": True
	},
	"(527328) 2007 TK422|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.710, "V-R": 0.510}, "sun": True
	},
	"(527443) 2007 UM126|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.740, "V-R": 0.435, "R-I": 0.440}, "sun": True
	},
	"(527603) 2007 VJ305|9": {"tags": ["solar_system", "minor_body", "tno", "detached"],
		"filters": "Landolt", "indices": {"B-V": 0.920, "V-R": 0.520, "R-I": 0.520}, "sun": True
	},
	"527604|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.830, "V-R": 0.470, "R-I": 0.480}, "sun": True
	},
	"(528219) 2008 KV42|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.820, "V-R": 0.470, "R-I": 0.420}, "sun": True
	},
	"530664|9": {"tags": ["solar_system", "minor_body", "tno", "scattered"],
		"filters": "Landolt", "indices": {"B-V": 0.690, "V-R": 0.390}, "sun": True
	},
	"530930|9": {"tags": ["solar_system", "minor_body", "asteroid", "centaur"],
		"filters": "Landolt", "indices": {"B-V": 0.720, "V-R": 0.400}, "sun": True
	},
    #"1998 KY26|9": {"filters": "Landolt", "indices": {"B-R": 0.083, "V-R": 0.058, "R-I": 0.088}, "sun": False},
    "Class A|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.708, 0.868, 1.109, 1.214, 1.298, 1.311, 1.250, 1.187, 1.143],
        "albedo": 0.274}, # https://arxiv.org/abs/1307.2424
    "Class B|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [1.008, 1.004, 0.989, 0.985, 0.978, 0.975, 0.969, 0.961, 0.938],
        "albedo": 0.071}, # https://arxiv.org/abs/1307.2424
    "Class C|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.936, 0.979, 1.007, 1.013, 1.014, 1.016, 1.014, 1.008, 0.993],
        "albedo": 0.083}, # https://arxiv.org/abs/1307.2424
    "Class Cb|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.981, 0.995, 0.999, 1.002, 1.002, 1.005, 1.003, 0.994, 0.979],
        "albedo": 0.083}, # https://arxiv.org/abs/1307.2424
    "Class Cg|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.852, 0.945, 1.018, 1.028, 1.027, 1.025, 1.026, 1.022, 1.007],
        "albedo": 0.083}, # https://arxiv.org/abs/1307.2424
    "Class Cgh|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.870, 0.962, 0.997, 0.985, 0.972, 0.973, 0.987, 0.991, 0.980],
        "albedo": 0.083}, # https://arxiv.org/abs/1307.2424
    "Class Ch|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.941, 0.986, 0.991, 0.983, 0.977, 0.982, 0.991, 0.996, 0.993],
        "albedo": 0.083}, # https://arxiv.org/abs/1307.2424
    "Class D|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.882, 0.951, 1.046, 1.098, 1.150, 1.199, 1.222, 1.247, 1.287],
        "albedo": 0.098}, # https://arxiv.org/abs/1307.2424
    "Class K|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.863, 0.943, 1.043, 1.087, 1.121, 1.138, 1.125, 1.110, 1.085],
        "albedo": 0.178}, # https://arxiv.org/abs/1307.2424
    "Class L|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.818, 0.922, 1.066, 1.130, 1.179, 1.207, 1.201, 1.193, 1.188],
        "albedo": 0.183}, # https://arxiv.org/abs/1307.2424
    "Class Ld|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.799, 0.913, 1.080, 1.163, 1.228, 1.270, 1.280, 1.282, 1.288],
        "albedo": 0.183}, # https://arxiv.org/abs/1307.2424
    "Class O|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.878, 0.952, 1.022, 1.042, 1.057, 1.036, 0.958, 0.870, 0.798]},
    "Class Q|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.830, 0.930, 1.047, 1.087, 1.118, 1.107, 1.041, 0.952, 0.873]},
    "Class R|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.792, 0.907, 1.073, 1.145, 1.209, 1.224, 1.110, 0.971, 0.889]},
    "Class S|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.813, 0.920, 1.060, 1.121, 1.170, 1.188, 1.145, 1.084, 1.034],
        "albedo": 0.258}, # https://arxiv.org/abs/1307.2424
    "Class Sa|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.748, 0.892, 1.094, 1.178, 1.243, 1.260, 1.216, 1.150, 1.091],
        "albedo": 0.258}, # https://arxiv.org/abs/1307.2424
    "Class Sk|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.859, 0.939, 1.039, 1.082, 1.115, 1.130, 1.092, 1.039, 1.001],
        "albedo": 0.258}, # https://arxiv.org/abs/1307.2424
    "Class Sl|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.790, 0.909, 1.076, 1.149, 1.209, 1.237, 1.205, 1.158, 1.131],
        "albedo": 0.258}, # https://arxiv.org/abs/1307.2424
    "Class Sq|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.851, 0.938, 1.039, 1.082, 1.115, 1.120, 1.069, 1.000, 0.936],
        "albedo": 0.258}, # https://arxiv.org/abs/1307.2424
    "Class Sr|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.777, 0.904, 1.069, 1.137, 1.188, 1.193, 1.123, 1.030, 0.936],
        "albedo": 0.258}, # https://arxiv.org/abs/1307.2424
    "Class T|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.896, 0.956, 1.041, 1.083, 1.119, 1.149, 1.163, 1.174, 1.184]},
    "Class V|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.808, 0.916, 1.063, 1.124, 1.176, 1.183, 1.048, 0.879, 0.745],
        "albedo": 0.352}, # https://arxiv.org/abs/1307.2424
    "Class X|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.940, 0.977, 1.013, 1.030, 1.045, 1.057, 1.062, 1.060, 1.058]},
    "Class Xc|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.920, 0.969, 1.019, 1.038, 1.049, 1.054, 1.047, 1.037, 1.020]},
    "Class Xe|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.921, 0.948, 1.032, 1.060, 1.082, 1.094, 1.093, 1.088, 1.078]},
    "Class Xk|7": {"nm": [440, 500, 600, 650, 700, 750, 800, 850, 920], "br": [0.900, 0.959, 1.033, 1.061, 1.084, 1.097, 1.098, 1.098, 1.098]},
    #"Comets|8": {"filters": "Landolt", "indices": {"B-V": 0.795, "V-R": 0.441, "V-I": 0.935}, "sun": True},
    "Comets:SP|9": {"filters": "Landolt", "indices": {"B-V": 0.87, "V-R": 0.50, "R-I": 0.45}, "sun": True},
    "Comets:LP|9": {"filters": "Landolt", "indices": {"B-V": 0.79, "V-R": 0.46, "R-I": 0.44}, "sun": True},
    #"J. trojans|8": {"filters": "Landolt", "indices": {"B-V": 0.777, "V-R": 0.445, "V-I": 0.861}, "sun": True},
    "J. trojans|9": {"filters": "Landolt", "indices": {"U-B": 0.1, "B-V": 0.78, "V-R": 0.45, "R-I": 0.42}, "sun": True},
    #"Centaurs|8": {"filters": "Landolt", "indices": {"B-V": 0.886, "V-R": 0.573, "V-I": 1.104}, "sun": True},
    "Centaurs|9": {"filters": "Landolt", "indices": {"B-V": 0.87, "V-R": 0.55, "R-I": 0.50}, "sun": True},
    #"Plutinos|8": {"filters": "Landolt", "indices": {"B-V": 0.895, "V-R": 0.568, "V-I": 1.095}, "sun": True},
    "Plutinos|9": {"filters": "Landolt", "indices": {"B-V": 0.88, "V-R": 0.55, "R-I": 0.53}, "sun": True},
    "Other res.|9": {"filters": "Landolt", "indices": {"U-B": 0.27, "B-V": 0.95, "V-R": 0.59, "R-I": 0.54}, "sun": True},
    #"Classic|8": {"filters": "Landolt", "indices": {"B-V": 0.973, "V-R": 0.622, "V-I": 1.181}, "sun": True},
    "Classic:H|9": {"filters": "Landolt", "indices": {"U-B": 0.27, "B-V": 0.88, "V-R": 0.54, "R-I": 0.53}, "sun": True},
    "Classic:C|9": {"filters": "Landolt", "indices": {"U-B": 0.59, "B-V": 1.00, "V-R": 0.63, "R-I": 0.59}, "sun": True},
    #"Scattered|8": {"filters": "Landolt", "indices": {"B-V": 0.875, "V-R": 0.553, "V-I": 1.070}, "sun": True},
    "Scattered|9": {"filters": "Landolt", "indices": {"U-B": 0.33, "B-V": 0.85, "V-R": 0.52, "R-I": 0.51}, "sun": True},
    "Detached|9": {"filters": "Landolt", "indices": {"U-B": 0.18, "B-V": 0.88, "V-R": 0.54, "R-I": 0.51}, "sun": True},
    "HD 189733 b|10": {"nm": [358.9, 437.2, 549.3], "br": [0.62, 0.61, 0.28], "albedo": True}
}

sources = [
    "[1]: CALSPEC calatog of stellar spectra (STScI)"
    "\nhttps://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec",
    "[2]: Comprehensive wide-band magnitudes and albedos for the planets, with applications to exo-planets and Planet Nine"
    "\nDOI: 10.1016/j.icarus.2016.09.023; https://www.sciencedirect.com/science/article/abs/pii/S0019103516301014",
    "[3]: Views from EPOXI: colors in our Solar system as an analog for extrasolar planets"
    "\nDOI: 10.1088/0004-637X/729/2/130; https://iopscience.iop.org/article/10.1088/0004-637X/729/2/130",
    "[4]: About the Spectra of the Planets and Satellites (USGS Archive)"
    "\nhttps://archive.usgs.gov/archive/sites/speclab.cr.usgs.gov/planetary.spectra/planetary-sp.html",
    "[5]: Spectrophotometry of the Jovian Planets and Titan at 300- to 1000-nm Wavelength: The Methane Spectrum"
    "\nDOI: 10.1006/icar.1994.1139; https://atmos.nmsu.edu/planetary_datasets/indexinfrared.html",
    "[6]: The Spectrum of Pluto, 0.40 - 0.93 um I. Secular and longitudinal distribution of ices and complex organics"
    "\nDOI: 10.1051/0004-6361/201527281; https://arxiv.org/abs/1509.00417",
    "[7]: Phase II of the Small Main-Belt Asteroid Spectroscopic Survey: A Feature-Based Taxonomy"
    "\nDOI: 10.1006/icar.2002.6856; https://www.sciencedirect.com/science/article/abs/pii/S0019103502968569",
    "[8]: Visible spectroscopic and photometric survey of Jupiter Trojans: final results on dynamical families"
    "\nDOI: 10.1016/j.icarus.2007.03.033; https://arxiv.org/abs/0704.0350",
    "[9]: Minor Bodies in the Outer Solar System: Magnitudes and Colours"
    "\nhttp://www.eso.org/~ohainaut/MBOSS/; http://www.eso.org/~ohainaut/MBOSS/mbossClasses.txt",
    "[10]: Polarized reflected light from the exoplanet HD189733b: First multicolor observations and confirmation of detection"
    "\nDOI: 10.1088/2041-8205/728/1/L6/; https://arxiv.org/abs/1101.0059",
    "[11]: Observations, compositional, and physical characterization of near-Earth and Mars-crosser asteroids from a spectroscopic survey"
    "\nDOI: 10.1051/0004-6361/200913852; https://ui.adsabs.harvard.edu/abs/2010A%26A...517A..23D/abstract",
    "[12]: Physical properties of Asteroid (25143) Itokawa — Target of the Hayabusa sample return mission"
    "\nDOI: 10.1016/j.icarus.2005.02.002; https://ui.adsabs.harvard.edu/abs/2005Icar..176..408L/abstract"
]