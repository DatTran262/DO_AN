        print("before")
        print(self.matrix)
        self.matrix = np.dot(self.matrix, rolled_by)
        print("after")
        print(self.matrix)