import { useEffect, useState } from 'react'
import { getFollowings } from '../../api/Friends'
import { refreshToken } from '../../api/User'
import FollowerCard from './FollowerCard'

const Followings = () => {
    const [followings, setFollowings] = useState({
        data: null,
    })
    useEffect(()=>{
        setFollowings({
            data: null,
        })
        getFollowings().then((response)=>{
            if (response.status === 401){
                refreshToken().then((response)=>{
                    if (response.status === 200){
                        console.log("success")
                        console.log(response.status)
                        getFollowings().then((response)=>{
                            if (response.status === 200){
                                setFollowings({
                                    data: response.data,
                                })
                            }
                            console.log("true");
                        })
                    }
                    else{
                        window.location.reload();
                        window.location.href = '/login';
                        
                    }
                })
            }else if (response.status === 200){
                setFollowings({
                    data: response.data,
                })
            }
        })
    }, [])

    let content = null;
    console.log(followings.data)
    if (followings.data){
        if (followings.data.length === 0){
            content = (<div className="none">No Following</div>)
        }
        else{
            content = followings.data.map((following, key)=>

            <FollowerCard follower={following}/>

            )
        }

    }

    return (
        <div>
            {content}
        </div>
    )
}
export default Followings;