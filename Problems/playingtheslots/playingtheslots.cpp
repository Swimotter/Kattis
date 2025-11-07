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
typedef pair<float, float> pff;
typedef vector<int> vi;
typedef vector<vi> vvi;

pff helper(pff p1, pff p2, pff p3) {
	float x = (p1.second - p2.second - (p1.second - p3.second) / (p1.first - p3.first) * p1.first - (p1.first - p3.first) / (p1.second - p3.second) * p2.first) / (- (p1.first - p3.first) / (p1.second - p3.second) - (p1.second - p3.second) / (p1.first - p3.first));
	float y = (p1.second - p3.second) / (p1.first - p3.first) * (x - p1.first) + p1.second;
	return pff(x,y);
}

float helper2(pff p1, pff p2) {
	return sqrtf(pow(p1.first - p2.first, 2) + pow(p1.second - p2.second, 2));
}

// NOTE: Oriented Minimum Bounding Box
void solve() {
	int n;
	cin >> n;

	vector<pff> points;
	REP(i, n) {
		float x,y;
		cin >> x >> y;
		points.push_back(pff(x, y));
	}

	float min = 100;
	REP(i, points.size()) {
		float cur = helper2(helper(points[i], points[(i + 2) % points.size()], points[(i + 1) % points.size()]), points[(i + 2) % points.size()]);
		if (cur < min) {
			min = cur;
		}
	}
	cout << format("{}", min);
}

int main() {
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	solve();
}
