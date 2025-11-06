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

void solve() {
	int p,a,b,c,d,n;
	cin >> p >> a >> b >> c >> d >> n;

	double cur;
	double max = p * (sin(a + b) + cos(c + d) + 2);
	double res;
	FOR(k, 2, n + 1) {
		cur = p * (sin(a * k + b) + cos(c * k + d) + 2);
		if (max - cur > res) {
			res = max - cur;
		}
		if (cur > max) {
			max = cur;
		}
	}
	cout << format("{}", res);
}

int main() {
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	solve();
}
