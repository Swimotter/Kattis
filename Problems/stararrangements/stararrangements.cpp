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

bool helper(int a, int b, int s, int c) {
	while (c < s) {
		c += a + b;
	}
	if (c == s) {
		return true;
	}

	c -= (a + b);
	c += a;

	return c == s;
}

void solve() {
	int s;
	cin >> s;

	cout << s << ":" << endl;
	FOR(i, 2, (s + 1) / 2 + 1) {
		int c = 0;

		if (helper(i, i - 1, s, 0)) {
			cout << i << "," << i - 1<< endl;
		}
		if (helper(i, i, s, 0)) {
			cout << i << "," << i << endl;
		}
	}
}

int main() {
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	solve();
}
