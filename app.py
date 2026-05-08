from flask import Flask, render_template, request

app = Flask(__name__)


def global_alignment(seq1, seq2, match=1, mismatch=-1, gap=-2):
    n = len(seq1)
    m = len(seq2)

    # Create scoring matrix
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize matrix
    for i in range(n + 1):
        dp[i][0] = i * gap

    for j in range(m + 1):
        dp[0][j] = j * gap

    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            diag = dp[i - 1][j - 1] + (
                match if seq1[i - 1] == seq2[j - 1] else mismatch
            )

            up = dp[i - 1][j] + gap
            left = dp[i][j - 1] + gap

            dp[i][j] = max(diag, up, left)

    # Traceback
    aligned1 = ""
    aligned2 = ""

    i = n
    j = m

    while i > 0 or j > 0:

        if (
            i > 0
            and j > 0
            and dp[i][j]
            == dp[i - 1][j - 1]
            + (
                match
                if seq1[i - 1] == seq2[j - 1]
                else mismatch
            )
        ):
            aligned1 = seq1[i - 1] + aligned1
            aligned2 = seq2[j - 1] + aligned2
            i -= 1
            j -= 1

        elif i > 0 and dp[i][j] == dp[i - 1][j] + gap:
            aligned1 = seq1[i - 1] + aligned1
            aligned2 = "-" + aligned2
            i -= 1

        else:
            aligned1 = "-" + aligned1
            aligned2 = seq2[j - 1] + aligned2
            j -= 1

    return dp[n][m], aligned1, aligned2


@app.route('/', methods=['GET', 'POST'])
def index():

    result = None

    if request.method == 'POST':

        seq1 = request.form['seq1'].upper().strip()
        seq2 = request.form['seq2'].upper().strip()

        match = int(request.form['match'])
        mismatch = int(request.form['mismatch'])
        gap = int(request.form['gap'])

        score, aligned1, aligned2 = global_alignment(
            seq1,
            seq2,
            match,
            mismatch,
            gap
        )

        result = {
            'score': score,
            'aligned1': aligned1,
            'aligned2': aligned2
        }

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)


