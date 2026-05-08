import sys

def global_alignment_score(seq1, seq2, match=1, mismatch=-1, gap=-2):
    n = len(seq1)
    m = len(seq2)

    # Initialize matrix
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Fill first row and column
    for i in range(n + 1):
        dp[i][0] = i * gap
    for j in range(m + 1):
        dp[0][j] = j * gap

    # Fill the matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                score_diag = dp[i - 1][j - 1] + match
            else:
                score_diag = dp[i - 1][j - 1] + mismatch

            score_up = dp[i - 1][j] + gap
            score_left = dp[i][j - 1] + gap

            dp[i][j] = max(score_diag, score_up, score_left)

    return dp[n][m]


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <sequence1> <sequence2>")
        return

    seq1 = sys.argv[1].upper()
    seq2 = sys.argv[2].upper()

    score = global_alignment_score(seq1, seq2)

    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")
    print(f"Global Alignment Score: {score}")


if __name__ == "__main__":
    main()