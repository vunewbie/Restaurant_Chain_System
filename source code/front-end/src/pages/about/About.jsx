import React from "react";
import styles from "./About.module.css";

const About = () => {
  return (
    <div className={styles.aboutContainer}>
      {/* Video YouTube */}
      <div className={styles.videoContainer}>
        <iframe
          width="100%"
          height="500"
          src="https://www.youtube.com/embed/bqmKNJpeTT4"
          frameBorder="0"
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          title="Video Giới Thiệu Vunewbie"
        ></iframe>
      </div>

      {/* Nội dung giới thiệu */}
      <div className={styles.contentContainer}>
        <h2>Về Chúng Tôi</h2>
        <p>
          Vunewbie là chuỗi nhà hàng sushi nổi tiếng tại Việt Nam, chuyên cung cấp các món sushi tươi ngon, chất lượng cao, được chế biến bởi đội ngũ đầu bếp tài năng và giàu kinh nghiệm. Với mục tiêu mang lại những trải nghiệm ẩm thực tuyệt vời và không gian sang trọng, ấm cúng, Vunewbie đã nhanh chóng chiếm được cảm tình của các thực khách trong và ngoài nước. 
        </p>
        <p>
          Nhà hàng Vunewbie hiện nay đã mở rộng quy mô với nhiều chi nhánh tại các thành phố lớn như Hồ Chí Minh, Hà Nội và Đà Nẵng. Mỗi chi nhánh của Vunewbie đều mang đến một không gian thư giãn, hiện đại và thoải mái, phù hợp với nhu cầu của khách hàng từ những bữa ăn gia đình ấm cúng đến các buổi tiệc sang trọng, hội nghị, hay những cuộc gặp gỡ bạn bè. Vunewbie luôn đặt chất lượng món ăn lên hàng đầu, đảm bảo nguồn nguyên liệu tươi ngon, an toàn và tốt cho sức khỏe.
        </p>
        <p>
          Chúng tôi đặc biệt chú trọng đến phong cách phục vụ chuyên nghiệp, tận tâm và thân thiện. Đội ngũ nhân viên tại Vunewbie luôn sẵn sàng phục vụ quý khách hàng với sự nhiệt tình và chu đáo, mang đến sự hài lòng tuyệt đối. Các món ăn tại Vunewbie được chế biến từ những nguyên liệu tươi sống, được tuyển chọn kỹ càng từ các nhà cung cấp uy tín, đảm bảo không chỉ có hương vị tuyệt vời mà còn an toàn cho sức khỏe của khách hàng.
        </p>
        <p>
          Vunewbie tự hào là nơi hội tụ của những món sushi đặc sắc, từ các loại sushi cuộn truyền thống đến các món sushi sáng tạo, được chế biến từ nhiều loại nguyên liệu phong phú như cá hồi, cá ngừ, tôm, mực, bạch tuộc, và nhiều loại hải sản tươi sống khác. Ngoài sushi, nhà hàng còn phục vụ các món ăn Nhật Bản đặc trưng khác như sashimi, tempura, ramen và các món lẩu Nhật, mang đến sự đa dạng trong thực đơn và đáp ứng nhu cầu ẩm thực của tất cả thực khách.
        </p>
        <p>
          Với sự phát triển không ngừng, Vunewbie đã trở thành điểm đến ưa thích của nhiều thực khách yêu thích ẩm thực Nhật Bản tại Việt Nam. Chúng tôi cam kết không ngừng nỗ lực để mang đến những bữa ăn ngon miệng, những trải nghiệm tuyệt vời cho khách hàng và sẽ tiếp tục mở rộng thêm nhiều chi nhánh trên khắp cả nước. Hãy đến và thưởng thức những món ăn tuyệt vời tại Vunewbie, nơi mang lại cho bạn cảm giác như đang thưởng thức ẩm thực Nhật Bản ngay tại Việt Nam.
        </p>
      </div>
    </div>
  );
};

export default About;
