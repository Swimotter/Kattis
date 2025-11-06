#include <bits/stdc++.h>
using namespace std;

#define REP(i, n) for (int i = 0; i < n; ++i)
#define REPD(i, n) for (int i = n - 1; i >= 0; --i)
#define FOR(i, a, b) for (int i = a; i < b; ++i)
#define FORD(i, a, b) for (int i = a - 1; i >= b; --i)
#define ALL(v) v.begin(), v.end()
typedef long long ll;
typedef unsigned long long ull;
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef vector<vi> vvi;

void solve() {
	string l;
	cin >> l;

	int m, s, e;
	m = s = e = 0;

	int r, b;
	int sr, sb;
	r = b = sr = sb = 0;
	REP(i, l.size()) {
		r += l[i] == 'R' ? 1 : -1;
		b += l[i] == 'B' ? 1 : -1;

		if (r > m) {
			m = r;
			s = sr + 1;
			e = i + 1;
		}
		if (b > m) {
			m = b;
			s = sb + 1;
			e = i + 1;
		}

		if (r < 0) {
			sr = i + 1;
			r = 0;
		}
		if (b < 0) {
			sb = i + 1;
			b = 0;
		}
	}

	cout << s << " " << e;
}

int main() {
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	solve();
}
