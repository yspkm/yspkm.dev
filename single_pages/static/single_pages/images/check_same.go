package main

import (
    "fmt"
    "io/ioutil"
)

func main(){
    fname0, fname1 := "building.jpg", "tmp_original.jpg"

    file0, err0 := ioutil.ReadFile(fname0);

    if err0 != nil {
        panic(err0);
    }

    file1, err1 := ioutil.ReadFile(fname1);

    if err1 != nil {
        panic(err0)
    }

    if len(file0) != len(file1){
        goto DIFF
    }

    for i := range file0 {
        if (file0[i] != file1[i]){
            goto DIFF
        }
    }
    fmt.Println("같은 파일")
    return

    DIFF:
    fmt.Println("다른 파일")
    return

}

