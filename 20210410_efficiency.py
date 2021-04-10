import math
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    #list_observed_original = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 12000] # ideal case
    #list_observed_original = [770,1512,2188,2774,3413,3904,4422,4711,5804] # without_mask
    #list_expected_original = [818,1643,2457,3256,4134,4982,5813,6575,9889] # without_mask

    list_expected_original = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 12000] 
    list_expected = [x / 2.0 for x in list_expected_original]


    list_observed_original = [905, 1810, 2605, 3341, 3998, 4579, 5140,5599,6713]
    list_observed = [x / 2.0 for x in list_observed_original]
    list_observed_minus = [x - math.sqrt(x) for x in list_observed]
    list_observed_plus = [x + math.sqrt(x) for x in list_observed]

    # horizontal axis: list_expected, vertical axis: list_observed_minus
    coefficients = np.polyfit(list_expected, list_observed, 5)
    coefficients_minus = np.polyfit(list_expected, list_observed_minus, 5)
    coefficients_plus = np.polyfit(list_expected, list_observed_plus, 5)

    # horizontal axis: list_observed_minus, vertical axis: list_expected
    coefficients_inv = np.polyfit(list_observed, list_expected, 5)
    coefficients_inv_minus = np.polyfit(list_observed_minus, list_expected, 5)
    coefficients_inv_plus = np.polyfit(list_observed_plus, list_expected, 5)

    #
    fig = plt.figure(figsize=(10, 10))
    plt.rcParams["font.size"] = 16
    ax = fig.add_subplot(1,1,1)
    #ax.scatter(list_expected, list_observed_plus)
    ax.scatter(list_expected, list_observed, s=40, c='black', marker="*", label ="N")
    #ax.scatter(list_expected, list_observed_minus)
    xs = np.linspace(500, 6000, 100)
    ys_plus = np.polyval(coefficients_plus,xs)
    ax.plot(xs, ys_plus, 'b-', lw=1, label="N + $sqrt(N)$")
    ys = np.polyval(coefficients, xs)
    ax.plot(xs, ys, 'r-', lw=1)
    ys_minus = np.polyval(coefficients_minus,xs)
    ax.plot(xs, ys_minus, 'g-', lw=1,label="N - $sqrt(N)$")
    ax.set_title('Detected track number vs track density')
    ax.set_xlabel(r'Track density [/$(100\mu m)^2$]')
    ax.set_ylabel('Detected track number')
    ax.legend()
    ax.grid(True)
    plt.ylim(0, list_observed[-1]*1.1)
    plt.xlim(0, list_expected[-1]*1.1)

    #
    plt.tight_layout()
    #
    #plt.show()
    plt.savefig("Detected_track_number_vs_track_density.png")
    #

    list_upper_error = []
    list_lower_error = []
    for i, x in enumerate(xs):
        y_this_plus = ys_plus[i]
        y_this_plus = ys_plus[i]
        y_this_minus = ys_minus[i]

        confirm_x_by_minus = np.polyval(coefficients_inv_minus, y_this_minus)
        confirm_x_by_plus = np.polyval(coefficients_inv_plus, y_this_plus)

        x_max =  np.polyval(coefficients_inv, y_this_plus)
        x_min =  np.polyval(coefficients_inv, y_this_minus)

        upper_error = (x_max - x) / x * 100
        lower_error = (x - x_min) / x * 100
        print(f"x={x}, x_min={x_min}, x_max={x_max}, upper_error={upper_error}, lower_error={lower_error}")
        list_upper_error.append(upper_error)
        list_lower_error.append(-lower_error)


    plt.clf()
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(xs, list_upper_error, s=6, c='black')
    ax.scatter(xs, list_lower_error, s=6, c='black')
    plt.ylim(-10,8)
    ax.set_title('Statistical error vs track density')
    ax.set_xlabel(r'Track density [/$(100\mu m)^2$]')
    ax.set_ylabel('Statistical error [%]')
    ax.grid(True)
    plt.tight_layout()
    #
    plt.savefig("Statistical_error_vs_track_density.png")
