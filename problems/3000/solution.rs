impl Solution {
    pub fn area_of_max_diagonal(dimensions: Vec<Vec<i32>>) -> i32 {
        let (mut best_diag, mut best_area) = (0, 0);
        for d in dimensions {
            let (length, width) = (d[0], d[1]);
            let diag = length * length + width * width;
            let area = length * width;
            if diag > best_diag || (diag == best_diag && area > best_area) {
                best_diag = diag;
                best_area = area;
            }
        }
        best_area
    }
}
