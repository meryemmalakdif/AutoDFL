// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library FixedPointMath {
    int256 constant ONE = 1e6; // 6 decimal places
    int256 constant TWO = 2e6;
    int256 constant LAMBDA = 1e3; // 10^-3 in fixed-point representation
    int256 constant MINUS_ONE = -1e6;
    int256 constant MAX_EXP_INPUT = 88e6; // Maximum input for the exp function to prevent overflow

    function exp(int256 x) internal pure returns (int256) {
        if (x < -MAX_EXP_INPUT) {
            return 0;
        } else if (x > MAX_EXP_INPUT) {
            return type(int256).max;
        }

        int256 sum = ONE;
        int256 term = ONE;
        for (uint256 i = 1; i < 100; i++) {
            term = (term * x) / (int256(i) * ONE);
            sum += term;
            if (term == 0) {
                break;
            }
        }
        return sum;
    }

    function tanh(int256 x) internal pure returns (int256) {
        if (x > MAX_EXP_INPUT) {
            return ONE;
        } else if (x < -MAX_EXP_INPUT) {
            return MINUS_ONE;
        }

        int256 exp2x = exp((TWO * x) / ONE);
        int256 numerator = exp2x - ONE;
        int256 denominator = exp2x + ONE;
        return (numerator * ONE) / denominator;
    }

    function tanhLambdaX(int256 x) internal pure returns (int256) {
        int256 scaledX = (x * LAMBDA) / ONE; // Scale x by lambda (10^-3)
        return tanh(scaledX);
    }
}